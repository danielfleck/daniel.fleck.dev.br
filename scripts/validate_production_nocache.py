#!/usr/bin/env python3
"""Valida produção com query única e headers no-cache."""

from __future__ import annotations
import argparse
import time
import urllib.parse
import urllib.request
import urllib.error

OLD_EMAIL = "danielfleck" + "@" + "gmail.com"
PUBLIC_EMAIL = "contato" + "@" + "fleck.dev.br"

EXPECTED = {
    "/": (
        'href="/privacidade/"',
        'href="/termos/"',
        'href="/contato/"',
    ),
    "/privacidade/": (
        "Aviso de Privacidade",
        "Versão 7",
        "contato [arroba] fleck.dev.br",
    ),
    "/termos/": (
        "Termos de Uso",
        "Versão 6",
        "/contato/",
    ),
    "/contato/": (
        "data-contact-open",
        "contato",
        "[arroba]",
    ),
    "/docs/": (
        "Documentação Técnica",
    ),
}

def unique(base: str, path: str) -> str:
    url = base.rstrip("/") + path
    parts = list(urllib.parse.urlsplit(url))
    query = urllib.parse.parse_qsl(parts[3], keep_blank_values=True)
    query.append(("__nocache", str(time.time_ns())))
    parts[3] = urllib.parse.urlencode(query)
    return urllib.parse.urlunsplit(parts)

def fetch(url: str):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "daniel-site-production-validator/2.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.status, response.headers, response.read().decode("utf-8", errors="replace")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="https://daniel.fleck.dev.br")
    args = parser.parse_args()

    errors = []
    for path, fragments in EXPECTED.items():
        url = unique(args.base_url, path)
        try:
            status, headers, body = fetch(url)
        except Exception as exc:
            errors.append(f"{path}: acesso falhou: {exc}")
            continue

        print(f"[{path}] HTTP {status}")
        for name in (
            "Date", "Age", "Via", "X-Cache", "X-Varnish",
            "Cache-Control", "ETag", "Last-Modified",
        ):
            if headers.get(name):
                print(f"  {name}: {headers.get(name)}")

        if status != 200:
            errors.append(f"{path}: status {status}")
        for fragment in fragments:
            if fragment not in body:
                errors.append(f"{path}: ausente {fragment!r}")

        if OLD_EMAIL in body:
            errors.append(f"{path}: e-mail antigo presente")
        if PUBLIC_EMAIL in body:
            errors.append(f"{path}: e-mail literal exposto no HTML")

    if errors:
        print("\nVALIDAÇÃO DE PRODUÇÃO: FALHOU")
        for error in errors:
            print("ERROR:", error)
        return 1

    print("\nVALIDAÇÃO DE PRODUÇÃO: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
