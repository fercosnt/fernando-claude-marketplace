#!/usr/bin/env python3
"""F4 stress tests: drive the parallel orchestrator with fake fetchers and a
fake NotebookLM CLI, assert (a) no work is lost, (b) the NCBI token bucket
throttles to <= the configured rate, (c) uploads are serialised end-to-end,
(d) parallel mode is measurably faster than --serial on the same fixture.

Run: python3 evals/test_parallel_fetching.py
"""
from __future__ import annotations

import os
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "scripts" / "sci_fetch"))
sys.path.insert(0, str(REPO / "scripts"))


def _isolate_cache() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="drsci_parallel_"))
    os.environ["DR_SCI_CACHE_ROOT"] = str(tmp)
    os.environ.pop("DR_SCI_NO_CACHE", None)
    os.environ["UNPAYWALL_EMAIL"] = "test@example.com"
    return tmp


def _reload():
    """Reload orchestrator + handlers after tweaking env / buckets."""
    import importlib
    for n in ("_cache", "_token_bucket", "_http", "classify_url",
              "pubmed_abstract", "pmc_fulltext", "pmid_to_pmc",
              "unpaywall_resolver", "open_access_pdf", "upload_to_nblm"):
        if n in sys.modules:
            del sys.modules[n]
    for n in ("_cache", "_token_bucket", "_http", "classify_url",
              "pubmed_abstract", "pmc_fulltext", "pmid_to_pmc",
              "unpaywall_resolver", "open_access_pdf", "upload_to_nblm"):
        importlib.import_module(n)


# ---------------------------------------------------------------------------
# Fake fetchers: record timestamp of each call, sleep a small amount to make
# parallelism observable, and return synthetic content of the right shape.
# ---------------------------------------------------------------------------
def _install_fakes(fetch_delay_sec: float = 0.05, *, throttle_ncbi: bool = False):
    """Install fakes. When `throttle_ncbi=True`, fakes call ncbi_throttle()
    before recording the timestamp so the token bucket limits show up in
    the observed call trace (mimicking the real fetch path)."""
    import pubmed_abstract, pmc_fulltext, pmid_to_pmc, upload_to_nblm
    from _http import ncbi_throttle

    ncbi_calls: list[float] = []
    lock = threading.Lock()

    big_body = "Relevant cohort data " * 400  # enough chars for PMC fulltext

    def fake_fetch_abstract(pmid, *, use_cache=True):
        if throttle_ncbi:
            ncbi_throttle()
        with lock:
            ncbi_calls.append(time.monotonic())
        time.sleep(fetch_delay_sec)
        return "Title\n\nAbstract body " * 30

    def fake_fetch_fulltext(pmcid, *, use_cache=True):
        if throttle_ncbi:
            ncbi_throttle()
        with lock:
            ncbi_calls.append(time.monotonic())
        time.sleep(fetch_delay_sec)
        return ("Study title", big_body)

    def fake_resolve_batch(pmids, *, use_cache=True):
        if throttle_ncbi:
            ncbi_throttle()
        with lock:
            ncbi_calls.append(time.monotonic())
        # elink is a single call per batch; don't throttle per-PMID.
        time.sleep(fetch_delay_sec)
        # Synthetic mapping: every PMID resolves to a PMC id.
        return {p: f"PMC{int(p)*7}" for p in pmids}

    pubmed_abstract.fetch_abstract = fake_fetch_abstract
    pmc_fulltext.fetch_fulltext = fake_fetch_fulltext
    pmid_to_pmc._resolve_batch = fake_resolve_batch

    # Re-point the orchestrator's bound references to the fakes.
    upload_to_nblm.pubmed_abstract.fetch_abstract = fake_fetch_abstract
    upload_to_nblm.pmc_fulltext.fetch_fulltext = fake_fetch_fulltext
    upload_to_nblm.pmid_to_pmc._resolve_batch = fake_resolve_batch

    # Stub NotebookLM CLI: record call timestamps + return ok; force the
    # uploader to take a tiny bit of wall time so serialisation is observable.
    upload_calls: list[tuple[float, str]] = []
    upload_lock = threading.Lock()
    upload_active = [0]

    def fake_add_file(file_path, notebook_id):
        # Detect whether >1 upload is happening at the same time; must be 0.
        concurrent = 0
        with upload_lock:
            upload_active[0] += 1
            concurrent = upload_active[0]
            upload_calls.append((time.monotonic(), str(file_path)))
        try:
            time.sleep(0.02)
        finally:
            with upload_lock:
                upload_active[0] -= 1
        if concurrent > 1:
            return {"ok": False, "source_id": None, "error": f"concurrent={concurrent}"}
        return {"ok": True, "source_id": "src_" + Path(file_path).stem, "error": None}

    def fake_add_url(url, notebook_id):
        concurrent = 0
        with upload_lock:
            upload_active[0] += 1
            concurrent = upload_active[0]
            upload_calls.append((time.monotonic(), url))
        try:
            time.sleep(0.02)
        finally:
            with upload_lock:
                upload_active[0] -= 1
        if concurrent > 1:
            return {"ok": False, "source_id": None, "error": f"concurrent={concurrent}"}
        return {"ok": True, "source_id": "url_" + url[-10:], "error": None}

    upload_to_nblm._nblm_add_file = fake_add_file
    upload_to_nblm._nblm_add_url = fake_add_url

    # Stub manifest.record_source so we don't touch disk.
    upload_to_nblm.manifest.record_source = lambda **kw: None

    # F4 isolation: scoring + bioRxiv fallback are tested in test_paper_scorer.py
    # and test_v3_apis.py respectively. Stub them here so the parallel orchestrator
    # tests don't accidentally hit live academic APIs (which would 429 us).
    # Stubbing score_paper at the orchestrator's binding short-circuits the
    # internal S2/OA/bioRxiv calls — no need to stub each API client separately.
    upload_to_nblm.paper_scorer.score_paper = lambda **kw: None
    upload_to_nblm.biorxiv_fallback.find_preprint = lambda doi, **kw: None

    return {"ncbi_calls": ncbi_calls, "upload_calls": upload_calls}


def _mk_pmids_urls(n: int) -> list[str]:
    return [f"https://pubmed.ncbi.nlm.nih.gov/{10_000_000 + i}/" for i in range(n)]


def _max_rate_per_second(timestamps: list[float]) -> float:
    """Return the peak requests-per-second observed across any 1s sliding
    window. 0 if there are fewer than 1 call."""
    if not timestamps:
        return 0.0
    ts = sorted(timestamps)
    best = 0
    j = 0
    for i in range(len(ts)):
        while ts[i] - ts[j] > 1.0:
            j += 1
        window = i - j + 1
        if window > best:
            best = window
    return float(best)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_parallel_all_uploaded():
    _isolate_cache()
    _reload()
    probe = _install_fakes(fetch_delay_sec=0.03)
    import upload_to_nblm

    urls = _mk_pmids_urls(20)
    work_dir = Path(tempfile.mkdtemp(prefix="drsci_work_parallel_"))

    summary = upload_to_nblm.process(
        urls=urls,
        notebook_id="nb_test",
        pesquisa_slug="stress",
        pesquisas_root=work_dir.parent,
        work_dir=work_dir,
        skip_upload=False,
        serial=False,
        max_parallel=9,  # 3/3/3 split
    )
    assert summary["total"] == 20
    assert summary["auto_uploaded"] == 20, f"expected 20 auto uploads, got {summary}"
    assert summary["manual_required"] == 0
    assert len(probe["upload_calls"]) == 20


def test_parallel_respects_ncbi_rate_limit():
    _isolate_cache()
    _reload()
    # Force the NCBI bucket to 3 req/s (the default without NCBI_API_KEY).
    os.environ.pop("NCBI_API_KEY", None)
    from _token_bucket import reset_buckets, get_bucket
    reset_buckets()

    # Fakes must honor ncbi_throttle() so timestamps reflect the bucket's
    # real gating, not free-running work.
    probe = _install_fakes(fetch_delay_sec=0.02, throttle_ncbi=True)
    import upload_to_nblm

    # Drain the initial burst so the bucket measures steady-state rate.
    b = get_bucket("ncbi")
    while b.tokens >= 1:
        b.acquire()

    urls = _mk_pmids_urls(20)
    work_dir = Path(tempfile.mkdtemp(prefix="drsci_rate_"))
    upload_to_nblm.process(
        urls=urls,
        notebook_id="nb_test",
        pesquisa_slug="rate",
        pesquisas_root=work_dir.parent,
        work_dir=work_dir,
        skip_upload=False,
        serial=False,
        max_parallel=9,
    )
    peak = _max_rate_per_second(probe["ncbi_calls"])
    # NCBI allows 3 req/s; our bucket has capacity=3 burst. Add 1 for timing
    # jitter across a 1s sliding window. Anything under 5 passes cleanly.
    assert peak <= 5, f"NCBI rate exceeded: peak={peak} req/s in 1s window"


def test_parallel_uploads_are_serialized():
    _isolate_cache()
    _reload()
    probe = _install_fakes(fetch_delay_sec=0.02)
    import upload_to_nblm

    urls = _mk_pmids_urls(15)
    work_dir = Path(tempfile.mkdtemp(prefix="drsci_serial_uploads_"))
    summary = upload_to_nblm.process(
        urls=urls,
        notebook_id="nb_test",
        pesquisa_slug="upsrl",
        pesquisas_root=work_dir.parent,
        work_dir=work_dir,
        skip_upload=False,
        serial=False,
        max_parallel=12,
    )
    # Fake uploader returns ok=False with error="concurrent=N" when two
    # invocations overlap. If the uploader thread is actually serial, ALL
    # uploads should succeed.
    assert summary["auto_uploaded"] == len(urls), (
        f"uploads overlapped (some returned concurrent=N error): {summary}"
    )


def test_parallel_is_faster_than_serial():
    _isolate_cache()
    _reload()
    _install_fakes(fetch_delay_sec=0.05)
    import upload_to_nblm

    urls = _mk_pmids_urls(15)

    t0 = time.monotonic()
    upload_to_nblm.process(
        urls=urls,
        notebook_id="nb1",
        pesquisa_slug="speed_serial",
        pesquisas_root=Path(tempfile.mkdtemp()),
        work_dir=Path(tempfile.mkdtemp()),
        skip_upload=False,
        serial=True,
    )
    serial_elapsed = time.monotonic() - t0

    # Fresh probe so we don't mix call logs.
    _isolate_cache()
    _reload()
    _install_fakes(fetch_delay_sec=0.05)
    import upload_to_nblm  # re-bind after reload
    t0 = time.monotonic()
    upload_to_nblm.process(
        urls=urls,
        notebook_id="nb2",
        pesquisa_slug="speed_parallel",
        pesquisas_root=Path(tempfile.mkdtemp()),
        work_dir=Path(tempfile.mkdtemp()),
        skip_upload=False,
        serial=False,
        max_parallel=9,
    )
    parallel_elapsed = time.monotonic() - t0

    # Expect at least 1.5x speedup; rate-limit + upload serialisation cap this
    # below the naive 9x. On a tiny fixture with 0.05s fake fetch latency,
    # 1.5x is already meaningful without being flaky.
    assert parallel_elapsed < serial_elapsed / 1.5, (
        f"parallel not significantly faster: parallel={parallel_elapsed:.2f}s "
        f"serial={serial_elapsed:.2f}s"
    )


def test_pool_sizes_default_and_override():
    _isolate_cache()
    _reload()
    from upload_to_nblm import _pool_sizes, DEFAULT_POOL_NCBI, DEFAULT_POOL_ACADEMIC, DEFAULT_POOL_GENERIC

    assert _pool_sizes(None) == (DEFAULT_POOL_NCBI, DEFAULT_POOL_ACADEMIC, DEFAULT_POOL_GENERIC)
    # N=10 → 30/30/40 → (3, 3, 4)
    assert _pool_sizes(10) == (3, 3, 4)
    # N=9 → (3, 3, 3)
    assert _pool_sizes(9) == (3, 3, 3)
    # N=1 → (1, 1, ...) floors at 1 each
    ncbi, academic, generic = _pool_sizes(1)
    assert (ncbi, academic) == (1, 1)
    assert generic >= 1


def run_all():
    tests = [
        test_pool_sizes_default_and_override,
        test_parallel_all_uploaded,
        test_parallel_uploads_are_serialized,
        test_parallel_respects_ncbi_rate_limit,
        test_parallel_is_faster_than_serial,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"  ok   {t.__name__}")
        except Exception as e:
            failures += 1
            import traceback
            print(f"  FAIL {t.__name__}: {e}")
            traceback.print_exc()
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all())
