#!/usr/bin/env python3
"""Atualiza somente as referências V5/V4 -> V6/V5 em scripts/validate.py.

O script é deliberadamente conservador: falha se as âncoras esperadas do HEAD
9fa42ee8927a663ab422290263ec86776fd8897a não forem encontradas.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "scripts" / "validate.py"

REPLACEMENTS = [
    ('"Versão 5",\n            "localStorage"', '"Versão 6",\n            "localStorage"'),
    ('Política V5 sem referência esperada', 'Política V6 sem referência esperada'),
    ('for required in ("Versão 4", "Web Storage", "/privacidade/", "Material for MkDocs")',
     'for required in ("Versão 5", "Web Storage", "/privacidade/", "Material for MkDocs")'),
    ('Termos V4 sem referência esperada', 'Termos V5 sem referência esperada'),
    ('Política de Privacidade: **Versão 5', 'Política de Privacidade: **Versão 6'),
    ('Termos de Uso: **Versão 4', 'Termos de Uso: **Versão 5'),
    ('Política de Privacidade: Versão 5', 'Política de Privacidade: Versão 6'),
    ('Termos de Uso: Versão 4', 'Termos de Uso: Versão 5'),
    ('Política de Privacidade pública **V5**', 'Política de Privacidade pública **V6**'),
    ('Termos de Uso públicos **V4**', 'Termos de Uso públicos **V5**'),
]

def main() -> int:
    if not TARGET.is_file():
        print("ERRO: scripts/validate.py não encontrado")
        return 2

    text = TARGET.read_text(encoding="utf-8")
    original = text

    for old, new in REPLACEMENTS:
        if old not in text:
            print("ERRO: âncora não encontrada:", old)
            return 2
        text = text.replace(old, new)

    if text == original:
        print("Nenhuma alteração realizada.")
        return 1

    TARGET.write_text(text, encoding="utf-8")
    print("ATUALIZADO: scripts/validate.py")
    print("Revise git diff antes de prosseguir.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
