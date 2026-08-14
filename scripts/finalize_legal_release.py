#!/usr/bin/env python3
"""Substitui o marcador de publicação da release jurídica.

Uso:
  python scripts/finalize_legal_release.py "13/08/2026 às 21:37 (BRT, UTC-3)"

Execute apenas quando tiver definido o horário que será registrado para a publicação.
Depois confira com grep e git diff antes do commit/push.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "__PUBLICATION_DATETIME__"

FILES = (
    ROOT / "site/privacidade/index.html",
    ROOT / "site/termos/index.html",
    ROOT / "mkdocs/docs/governanca/index.md",
    ROOT / "mkdocs/docs/governanca/controle-versoes-documentos-legais.md",
)

def main() -> int:
    if len(sys.argv) != 2:
        print('Uso: python scripts/finalize_legal_release.py "DD/MM/AAAA às HH:MM (BRT, UTC-3)"')
        return 2

    value = sys.argv[1].strip()
    if not value:
        print("ERRO: data/hora vazia")
        return 2

    missing = [str(p.relative_to(ROOT)) for p in FILES if not p.is_file()]
    if missing:
        print("ERRO: arquivos ausentes:", ", ".join(missing))
        return 2

    changed = 0
    for path in FILES:
        text = path.read_text(encoding="utf-8")
        if MARKER in text:
            path.write_text(text.replace(MARKER, value), encoding="utf-8")
            print("ATUALIZADO:", path.relative_to(ROOT))
            changed += 1

    if changed == 0:
        print("AVISO: nenhum marcador encontrado; verifique se a release já foi finalizada.")
    else:
        print("OK. Revise git diff antes do commit.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
