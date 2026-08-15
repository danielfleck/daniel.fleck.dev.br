#!/usr/bin/env python3
"""Lembrete/gate de conformidade executado em todo commit.

O script NÃO consulta a internet e NÃO certifica conformidade jurídica.
Ele:
- informa a idade da última revisão completa;
- avisa quando a revisão trimestral se aproxima/atrasa;
- bloqueia commits quando o atraso excede a tolerância configurada;
- exige racional junto a alteração jurídica material;
- lembra os gatilhos de privacidade quando arquivos sensíveis mudam.
"""

from __future__ import annotations
import argparse
import json
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "governance" / "compliance-status.json"

TRIGGERS = (
    "site/",
    "templates/",
    "mkdocs/",
    "scripts/",
    ".githooks/",
)
LEGAL = ("site/privacidade/", "site/termos/")
CONTACT = (
    "contato",
    "site_config.py",
    "footer.html",
    "main.js",
)

def git_staged() -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]

def parse_date(value: str) -> date:
    return date.fromisoformat(value)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    if not STATUS.is_file():
        print("COMPLIANCE: status ausente:", STATUS.relative_to(ROOT))
        return 1 if args.enforce else 0

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    today = date.today()
    last = parse_date(data["last_full_review"])
    next_review = parse_date(data["next_full_review"])
    warning_days = int(data.get("warning_days_before", 15))
    max_overdue = int(data.get("maximum_overdue_days", 30))

    age = (today - last).days
    until = (next_review - today).days

    print(
        f"COMPLIANCE: última revisão completa={last.isoformat()} "
        f"({age} dias); próxima={next_review.isoformat()}."
    )
    print(
        "COMPLIANCE: lembrete — este gate verifica documentação/local, "
        "não confirma sozinho a vigência das normas na internet."
    )

    if until <= warning_days and until >= 0:
        print(f"COMPLIANCE: revisão completa vence em {until} dia(s).")
    elif until < 0:
        overdue = abs(until)
        print(f"COMPLIANCE: revisão completa ATRASADA há {overdue} dia(s).")
        if args.enforce and overdue > max_overdue:
            print(
                "COMPLIANCE: commit bloqueado. Faça a revisão completa e execute "
                "scripts/ack_compliance_review.py."
            )
            return 1

    paths = git_staged() if args.staged else []
    relevant = [p for p in paths if p.startswith(TRIGGERS)]
    if relevant:
        print("COMPLIANCE: mudança relevante detectada. Antes do commit, confira:")
        print("  - o Aviso de Privacidade ainda descreve o comportamento real?")
        print("  - surgiu novo host externo, formulário, analytics, CDN, pixel ou storage?")
        print("  - contato/e-mail/fornecedor/retenção mudaram?")
        print("  - CSP, headers, /docs e auditoria de rede continuam coerentes?")
        print("  - o racional e o SCRIPTS.md precisam ser atualizados?")

    legal_changed = [p for p in paths if p.startswith(LEGAL)]
    if legal_changed:
        rationale_changed = any(
            p.startswith("mkdocs/docs/conformidade/racional-")
            or p.endswith("controle-versoes-documentos-legais.md")
            for p in paths
        )
        if not rationale_changed:
            print(
                "COMPLIANCE: documento jurídico alterado sem racional/controle "
                "de versão no mesmo staged diff."
            )
            return 1 if args.enforce else 0

    contact_changed = [
        p for p in paths
        if any(token in p.lower() for token in CONTACT)
    ]
    if contact_changed:
        print(
            "COMPLIANCE: mudança de contato detectada; verificar ofuscação, "
            "modal, fornecedor, retenção, SPF/DKIM/DMARC e referências."
        )

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
