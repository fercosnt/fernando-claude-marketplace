#!/usr/bin/env python3
"""Conta aprovação sem × com refação a partir das concluídas do período (Q11).

Uso: python3 faixas_refacao.py linhas.json
     linhas.json = lista de objetos com 'Entrou em aprovação em', 'Refações',
     'Tipo de entrega', 'Empresa' (e opcionalmente 'Pilar de conteúdo').
Regra (formulas-espelho #16b): só entra quem passou por aprovação a partir de
2026-09-21. Sem carimbo = fora do recorte (não é "sem refação"). Nunca agrupa
por Responsável — o campo nem é lido.
"""
import json, sys
from collections import defaultdict

INICIO = "2026-09-21"
FAIXAS = ["Sem refação", "1 volta", "2 voltas", "3+"]

def faixa(r):
    a = r.get("Entrou em aprovação em")
    if not a or a[:10] < INICIO:
        return None
    n = r.get("Refações") or 0
    return "Sem refação" if n <= 0 else "1 volta" if n == 1 else "2 voltas" if n == 2 else "3+"

def main(path):
    linhas = json.load(open(path))
    if isinstance(linhas, dict):
        linhas = linhas.get("linhas") or linhas.get("results") or []
    cortes = {"Total": lambda r: "Total", "Tipo de entrega": lambda r: r.get("Tipo de entrega") or "—",
              "Empresa": lambda r: r.get("Empresa") or "—", "Pilar": lambda r: r.get("Pilar de conteúdo") or "(sem pilar)"}
    fora = sum(1 for r in linhas if faixa(r) is None)
    out = {"fora_do_recorte_sem_aprovacao": fora}
    for nome, chave in cortes.items():
        g = defaultdict(lambda: dict.fromkeys(FAIXAS, 0))
        for r in linhas:
            f = faixa(r)
            if f:
                g[chave(r)][f] += 1
        tab = {}
        for k, c in sorted(g.items()):
            tot = sum(c.values()); com = tot - c["Sem refação"]
            tab[k] = {"com_aprovacao": tot, "sem_refacao": c["Sem refação"], "com_refacao": com,
                      **{f: c[f] for f in FAIXAS[1:]},
                      "pct_sem_refacao": round(100 * c["Sem refação"] / tot) if tot else None}
        out[nome] = tab
    print(json.dumps(out, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main(sys.argv[1])
