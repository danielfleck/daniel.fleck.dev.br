#!/usr/bin/env python3
"""Valida que o e-mail público não voltou a ficar trivialmente exposto no HTML."""

from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
TEMPLATES = ROOT / "templates"

OLD = "danielfleck" + "@" + "gmail.com"
PUBLIC_LITERAL = "contato" + "@" + "fleck.dev.br"

def source_files():
    docs = (SITE / "docs").resolve()
    for root in (SITE, TEMPLATES):
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".html", ".xml", ".txt"}:
                continue
            if root == SITE:
                try:
                    path.resolve().relative_to(docs)
                    continue
                except ValueError:
                    pass
            yield path

def main() -> int:
    errors = []

    contact = SITE / "contato" / "index.html"
    if not contact.is_file():
        errors.append("site/contato/index.html ausente")
    else:
        text = contact.read_text(encoding="utf-8")
        for required in (
            "data-contact-open",
            "contato",
            "[arroba]",
            "/privacidade/",
            "/termos/",
        ):
            if required not in text:
                errors.append(f"/contato/ sem {required}")
        if PUBLIC_LITERAL in text or f"mailto:{PUBLIC_LITERAL}" in text:
            errors.append("/contato/ expõe e-mail literal no HTML")

    for path in source_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if OLD in text:
            errors.append(f"e-mail antigo em {path.relative_to(ROOT)}")
        if PUBLIC_LITERAL in text:
            errors.append(
                f"e-mail público literal em {path.relative_to(ROOT)}; "
                "use /contato/ ou forma ofuscada"
            )

    curriculum = SITE / "curriculo.html"
    if curriculum.is_file():
        curriculum_text = curriculum.read_text(encoding="utf-8", errors="ignore")
        for required in (
            'property="og:title"',
            'property="og:url"',
            '/js/main.js',
            '/privacidade/',
            '/termos/',
            '/seguranca/',
            '/contato/',
        ):
            if required not in curriculum_text:
                errors.append(f"site/curriculo.html sem requisito atual: {required}")

    main_js = SITE / "js" / "main.js"
    if not main_js.is_file() or "PRIVACY-LINK-GUARD" not in main_js.read_text(encoding="utf-8"):
        errors.append("site/js/main.js sem PRIVACY-LINK-GUARD")

    if errors:
        print("CONTATO/EMAIL: FALHOU")
        for error in errors:
            print("ERROR:", error)
        return 1
    print("CONTATO/EMAIL: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
