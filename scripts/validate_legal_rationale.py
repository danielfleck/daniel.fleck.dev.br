#!/usr/bin/env python3
"""Valida comentários/racionais da release jurídica V7/V6."""

from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVACY = ROOT / "site" / "privacidade" / "index.html"
TERMS = ROOT / "site" / "termos" / "index.html"

DOCS = (
    ROOT / "mkdocs/docs/conformidade/racional-aviso-privacidade-v7.md",
    ROOT / "mkdocs/docs/conformidade/racional-termos-uso-v6.md",
    ROOT / "mkdocs/docs/conformidade/matriz-fontes-e-evidencias.md",
    ROOT / "mkdocs/docs/conformidade/politica-interna-privacidade.md",
    ROOT / "mkdocs/docs/conformidade/politica-retencao-descarte.md",
    ROOT / "mkdocs/docs/conformidade/transporte-https-hsts-security-txt.md",
    ROOT / "mkdocs/docs/conformidade/procedimento-relato-vulnerabilidade.md",
    ROOT / "mkdocs/docs/conformidade/diligencia-kinghost-pendente.md",
)

def check_html(path: Path, prefix: str, count: int) -> list[str]:
    errors = []
    if not path.is_file():
        return [f"ausente: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    if "AI-LEGAL-RATIONALE" not in text:
        errors.append(f"{path.relative_to(ROOT)} sem AI-LEGAL-RATIONALE")
    for number in range(1, count + 1):
        marker = f"LEGAL-RATIONALE:{prefix}:{number:02d}"
        if marker not in text:
            errors.append(f"{path.relative_to(ROOT)} sem {marker}")
    return errors

def main() -> int:
    errors = []
    errors += check_html(PRIVACY, "PRIVACY", 16)
    errors += check_html(TERMS, "TERMS", 18)
    for path in DOCS:
        if not path.is_file():
            errors.append(f"racional/governança ausente: {path.relative_to(ROOT)}")

    if errors:
        print("RACIONAL LEGAL: FALHOU")
        for error in errors:
            print("ERROR:", error)
        return 1
    print("RACIONAL LEGAL: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
