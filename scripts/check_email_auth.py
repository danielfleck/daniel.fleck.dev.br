#!/usr/bin/env python3
"""Analisa cabeçalhos de mensagem entregue para SPF/DKIM/DMARC.

Não valida criptograficamente a mensagem; interpreta resultados adicionados pelo receiver.
Use em uma cópia .eml privada e NÃO faça commit do arquivo.
"""

from __future__ import annotations
import argparse
import re
from email import policy
from email.parser import BytesParser
from pathlib import Path

ORG_DOMAIN = "fleck.dev.br"

def aligned(domain: str | None) -> bool:
    if not domain:
        return False
    domain = domain.lower().strip(".")
    return domain == ORG_DOMAIN or domain.endswith("." + ORG_DOMAIN)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("eml", type=Path)
    args = parser.parse_args()

    msg = BytesParser(policy=policy.default).parsebytes(args.eml.read_bytes())
    from_value = str(msg.get("From", ""))
    return_path = str(msg.get("Return-Path", ""))
    auth_headers = msg.get_all("Authentication-Results", [])
    dkim_headers = msg.get_all("DKIM-Signature", [])

    print("From:", from_value)
    print("Return-Path:", return_path)
    print()

    if not auth_headers:
        print("AVISO: nenhum Authentication-Results encontrado.")
    else:
        print("Authentication-Results:")
        for value in auth_headers:
            print(" ", " ".join(str(value).split()))

    d_domains = []
    for value in dkim_headers:
        match = re.search(r"(?:^|;)\s*d=([^;\s]+)", str(value), re.I)
        if match:
            d_domains.append(match.group(1))

    print()
    print("DKIM d= encontrados:", ", ".join(d_domains) if d_domains else "(nenhum)")
    if d_domains:
        print("DKIM alinhado com fleck.dev.br:", any(aligned(d) for d in d_domains))

    auth_text = " ".join(str(v) for v in auth_headers).lower()
    for mechanism in ("spf", "dkim", "dmarc"):
        results = re.findall(rf"\b{mechanism}=([a-z0-9_-]+)", auth_text)
        print(f"{mechanism.upper()} resultados:", ", ".join(results) if results else "(não localizado)")

    if "dmarc=pass" in auth_text:
        print("\nRESULTADO: o receiver registrou DMARC=pass.")
        return 0

    print(
        "\nRESULTADO: não foi localizado DMARC=pass. "
        "Não avance DMARC para enforcement com base apenas neste teste."
    )
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
