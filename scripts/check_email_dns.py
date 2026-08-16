#!/usr/bin/env python3
"""Confere SPF/DMARC publicados usando `dig`.

Não altera DNS. Requer o comando `dig` instalado.
"""

from __future__ import annotations
import shutil
import subprocess
import sys

DOMAIN = "fleck.dev.br"
EXPECTED_SPF = "v=spf1 include:_spf.kinghost.net -all"

def query(name: str) -> list[str]:
    proc = subprocess.run(
        ["dig", "+short", "TXT", name],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "dig falhou")
    return [line.strip().strip('"') for line in proc.stdout.splitlines() if line.strip()]

def main() -> int:
    if not shutil.which("dig"):
        print("ERRO: comando `dig` não encontrado.")
        return 2

    spf_records = [x for x in query(DOMAIN) if "v=spf1" in x.lower()]
    dmarc_records = query("_dmarc." + DOMAIN)

    print("SPF:")
    for record in spf_records:
        print(" ", record)
    if len(spf_records) != 1:
        print("ALERTA: deve haver um único registro SPF.")
    elif spf_records[0] != EXPECTED_SPF:
        print("AVISO: SPF difere do estado documentado; revisar antes de alterar.")

    print("\nDMARC:")
    for record in dmarc_records:
        print(" ", record)

    if not any("v=DMARC1" in r for r in dmarc_records):
        print("ALERTA: DMARC não localizado.")
        return 1
    if any("p=none" in r and "rua=" not in r for r in dmarc_records):
        print("INFO: p=none sem rua; não há solicitação de relatórios agregados para você.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
