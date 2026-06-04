"""Tests for notebook_manifest._touch_pesquisa fix (G1).

Regression: `_touch_pesquisa` used to call `resolved.relative_to(Path.cwd())`
without handling ValueError. When `pesquisas_root` was absolute and outside
the current working directory (e.g. `--pesquisas-root /tmp/...`), each
`record_source()` call raised ValueError. `upload_to_nblm._upload_and_record`
caught it and only logged `[warn] manifest update for <url>: ...`, so the
manifest silently never persisted. These tests pin down the contract that
`record_source()` works for work_dirs inside cwd, outside cwd (absolute),
and relative — across repeated calls (upsert path too).
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # .../deep-research/
sys.path.insert(0, str(ROOT / "scripts"))

import notebook_manifest as nm  # noqa: E402


class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors: list[str] = []

    def ok(self, name: str) -> None:
        self.passed += 1
        print(f"PASS  {name}")

    def fail(self, name: str, err: str) -> None:
        self.failed += 1
        self.errors.append(f"{name}: {err}")
        print(f"FAIL  {name}: {err}")

    def summary(self) -> int:
        total = self.passed + self.failed
        print(f"\n{total} tests | {self.failed} failures")
        return 0 if self.failed == 0 else 1


def _record_one(manifest_path: Path, pesquisas_root: Path, slug: str, canonical: str) -> dict:
    return nm.record_source(
        manifest_path=manifest_path,
        notebook_id="nb-test",
        pesquisa_slug=slug,
        pesquisas_root=pesquisas_root,
        canonical_key=canonical,
        title=f"Title for {canonical}",
        source_type="article",
        origin_pesquisa=slug,
        status="ok",
        ingest_method="url_direct",
    )


def test_absolute_pesquisas_root_inside_cwd(r: TestResult) -> None:
    """When pesquisas_root is absolute and inside cwd → path is stored relative to cwd."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            pesquisas_root = (tmp_path / "pesquisas").resolve()
            pesquisas_root.mkdir()
            manifest = pesquisas_root / "_notebook-manifest.json"
            _record_one(manifest, pesquisas_root, "slug-a", "doi:10.x/y")
            data = json.loads(manifest.read_text())
            path = data["notebooks"]["nb-test"]["pesquisas"][0]["path"]
            assert not Path(path).is_absolute(), f"expected relative path, got {path}"
            assert path.endswith("slug-a"), f"path missing slug: {path}"
            r.ok("absolute_root_inside_cwd_stores_relative")
        except Exception as e:
            r.fail("absolute_root_inside_cwd_stores_relative", str(e))
        finally:
            os.chdir(orig_cwd)


def test_absolute_pesquisas_root_outside_cwd(r: TestResult) -> None:
    """G1 REGRESSION: absolute pesquisas_root outside cwd must NOT raise; path is absolute."""
    with tempfile.TemporaryDirectory() as cwd_tmp, tempfile.TemporaryDirectory() as outside_tmp:
        orig_cwd = os.getcwd()
        try:
            os.chdir(cwd_tmp)  # cwd is now somewhere else
            pesquisas_root = Path(outside_tmp).resolve()  # absolute, outside cwd
            manifest = pesquisas_root / "_notebook-manifest.json"
            src = _record_one(manifest, pesquisas_root, "regression-v2-cold", "pmc:PMC123")
            assert src is not None and src["canonical_key"] == "pmc:PMC123"
            assert manifest.exists(), "manifest was not written"
            data = json.loads(manifest.read_text())
            path = data["notebooks"]["nb-test"]["pesquisas"][0]["path"]
            assert Path(path).is_absolute(), f"expected absolute path, got {path}"
            assert path.endswith("regression-v2-cold"), f"path missing slug: {path}"
            # Source actually landed in manifest.
            sources = data["notebooks"]["nb-test"]["sources"]
            assert len(sources) == 1 and sources[0]["canonical_key"] == "pmc:PMC123"
            r.ok("absolute_root_outside_cwd_does_not_raise")
        except Exception as e:
            r.fail("absolute_root_outside_cwd_does_not_raise", str(e))
        finally:
            os.chdir(orig_cwd)


def test_relative_pesquisas_root(r: TestResult) -> None:
    """Relative pesquisas_root is stored verbatim (no resolve/relative_to dance)."""
    with tempfile.TemporaryDirectory() as tmp:
        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp)
            (Path(tmp) / "pesquisas").mkdir()
            pesquisas_root = Path("pesquisas")  # relative
            manifest = pesquisas_root / "_notebook-manifest.json"
            _record_one(manifest, pesquisas_root, "slug-rel", "pmid:12345")
            data = json.loads(manifest.read_text())
            path = data["notebooks"]["nb-test"]["pesquisas"][0]["path"]
            assert not Path(path).is_absolute(), f"expected relative, got {path}"
            assert path == "pesquisas/slug-rel", f"unexpected path: {path}"
            r.ok("relative_root_stored_verbatim")
        except Exception as e:
            r.fail("relative_root_stored_verbatim", str(e))
        finally:
            os.chdir(orig_cwd)


def test_upsert_multiple_sources_outside_cwd(r: TestResult) -> None:
    """Multiple record_source calls with absolute outside-cwd root — all persist, last_delta_at updates."""
    with tempfile.TemporaryDirectory() as cwd_tmp, tempfile.TemporaryDirectory() as outside_tmp:
        orig_cwd = os.getcwd()
        try:
            os.chdir(cwd_tmp)
            pesquisas_root = Path(outside_tmp).resolve()
            manifest = pesquisas_root / "_notebook-manifest.json"
            _record_one(manifest, pesquisas_root, "regression", "doi:10.a/b")
            _record_one(manifest, pesquisas_root, "regression", "doi:10.c/d")
            _record_one(manifest, pesquisas_root, "regression", "doi:10.a/b")  # upsert
            data = json.loads(manifest.read_text())
            sources = data["notebooks"]["nb-test"]["sources"]
            canonicals = sorted(s["canonical_key"] for s in sources)
            assert canonicals == ["doi:10.a/b", "doi:10.c/d"], f"bad sources: {canonicals}"
            upserted = next(s for s in sources if s["canonical_key"] == "doi:10.a/b")
            assert upserted["attempts"] == 2, f"expected 2 attempts on upsert, got {upserted['attempts']}"
            pesquisas = data["notebooks"]["nb-test"]["pesquisas"]
            assert len(pesquisas) == 1 and pesquisas[0]["slug"] == "regression"
            r.ok("upsert_multiple_sources_outside_cwd")
        except Exception as e:
            r.fail("upsert_multiple_sources_outside_cwd", str(e))
        finally:
            os.chdir(orig_cwd)


def main() -> int:
    r = TestResult()
    test_absolute_pesquisas_root_inside_cwd(r)
    test_absolute_pesquisas_root_outside_cwd(r)
    test_relative_pesquisas_root(r)
    test_upsert_multiple_sources_outside_cwd(r)
    return r.summary()


if __name__ == "__main__":
    sys.exit(main())
