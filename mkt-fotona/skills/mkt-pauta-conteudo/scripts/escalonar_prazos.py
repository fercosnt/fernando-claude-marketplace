#!/usr/bin/env python3
"""Escalona os prazos das fases de uma peça de conteúdo a partir da Data planejada (D0).

Uso:
  python3 escalonar_prazos.py 2026-10-15 carrossel
  python3 escalonar_prazos.py 2026-10-15 reels --json
  python3 escalonar_prazos.py 2026-10-13 carrossel --feriados 2026-10-12,2026-11-02

Regras (shared/conteudo.md, decididas em 06/09/2026):
  - Não-vídeo: Roteiro D-7 · Arte/Edição D-4 · Legenda D-2 · Aprovação D-1 · Postagem D0
  - Vídeo:     Roteiro D-10 · Gravação D-7 · Arte/Edição D-4 · Legenda D-2 · Aprovação D-1 · Postagem D0
  - Prazo em sábado/domingo recua para a sexta anterior; prazo em feriado (--feriados) recua para o
    dia útil anterior (a mesma lógica: fim de semana e feriado não são dia de entrega).
  - A mãe recebe Prazo interno = D-1 (com a mesma regra de fim de semana) e NÃO recebe Prazo.

Os dias são parâmetros: se o coordenador de criação mudar a tabela no conteudo.md, mude aqui também
(ou passe --offsets "Roteiro:-7,Arte/Edição:-4,...").
"""
import argparse
import datetime as dt
import json
import sys

FASES_PADRAO = [("Roteiro", -7), ("Arte/Edição", -4), ("Legenda", -2), ("Aprovação", -1), ("Postagem", 0)]
FASES_VIDEO = [("Roteiro", -10), ("Gravação", -7), ("Arte/Edição", -4), ("Legenda", -2), ("Aprovação", -1), ("Postagem", 0)]

FORMATOS_VIDEO = {"reels", "reel", "vídeo", "video", "vídeo curto", "video curto", "vídeo longo", "video longo",
                  "youtube", "short", "shorts", "institucional", "tiktok", "vídeo institucional"}


def eh_video(formato: str) -> bool:
    f = formato.strip().lower()
    return f in FORMATOS_VIDEO or "vídeo" in f or "video" in f or "reel" in f


def recua_dia_util(d: dt.date, feriados=frozenset()) -> dt.date:
    """Sábado, domingo e feriado recuam para o dia útil anterior (sexta, ou o dia antes do feriado)."""
    while d.weekday() >= 5 or d in feriados:
        d -= dt.timedelta(days=1)
    return d


# compatibilidade com o nome antigo
recua_fim_de_semana = recua_dia_util


def escalonar(data_planejada: dt.date, formato: str, offsets=None, feriados=frozenset()):
    fases = offsets or (FASES_VIDEO if eh_video(formato) else FASES_PADRAO)
    out = []
    for nome, off in fases:
        bruto = data_planejada + dt.timedelta(days=off)
        prazo = recua_dia_util(bruto, feriados)
        motivo = "" if prazo == bruto else ("feriado" if bruto in feriados else "fim de semana")
        out.append({"fase": nome, "offset": off, "prazo_bruto": bruto.isoformat(),
                    "prazo": prazo.isoformat(), "recuou_por": motivo})
    mae = recua_dia_util(data_planejada - dt.timedelta(days=1), feriados).isoformat()
    aviso = ""
    if data_planejada.weekday() >= 5 or data_planejada in feriados:
        aviso = "ATENÇÃO: a própria Data planejada cai em fim de semana ou feriado — confirme com a pessoa (postagem pode ser intencional)."
    return {"data_planejada": data_planejada.isoformat(), "formato": formato, "video": eh_video(formato),
            "feriados": sorted(f.isoformat() for f in feriados), "prazo_interno_mae": mae, "fases": out, "aviso": aviso}


def parse_offsets(s: str):
    pares = []
    for item in s.split(","):
        nome, off = item.rsplit(":", 1)
        pares.append((nome.strip(), int(off)))
    return pares


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_planejada", help="AAAA-MM-DD")
    ap.add_argument("formato", help="carrossel, reels, story, artigo, ...")
    ap.add_argument("--offsets", help='ex.: "Roteiro:-7,Arte/Edição:-4,Legenda:-2,Aprovação:-1,Postagem:0"')
    ap.add_argument("--feriados", help="datas AAAA-MM-DD separadas por vírgula (feriados que caem no período)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    d0 = dt.date.fromisoformat(a.data_planejada)
    feriados = frozenset(dt.date.fromisoformat(x.strip()) for x in a.feriados.split(",")) if a.feriados else frozenset()
    r = escalonar(d0, a.formato, parse_offsets(a.offsets) if a.offsets else None, feriados)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    print(f"Data planejada (D0): {r['data_planejada']}  ·  formato: {r['formato']} ({'vídeo → 6 fases' if r['video'] else '5 fases'})")
    print(f"Prazo interno da mãe (D-1): {r['prazo_interno_mae']}")
    if r["aviso"]:
        print(r["aviso"])
    for f in r["fases"]:
        ajuste = "" if not f["recuou_por"] else f"  (recuou de {f['prazo_bruto']}, {f['recuou_por']})"
        print(f"  {f['fase']:<12} D{f['offset']:+d}  → {f['prazo']}{ajuste}")


if __name__ == "__main__":
    main()
