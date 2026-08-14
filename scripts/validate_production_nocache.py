#!/usr/bin/env python3
"""Valida a produção evitando depender de cache do crawler ou do navegador.

Usa:
- query string única por requisição;
- Cache-Control: no-cache, no-store, max-age=0;
- Pragma: no-cache;
- validação de conteúdo e response headers.

Não substitui a auditoria Playwright de rede.
"""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

EXPECTED = {
    "/": {
        "body": ('href="/privacidade/"', 'href="/termos/"', "Privacidade:"),
        "headers": {
            "Referrer-Policy": "no-referrer",
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "frame-ancestors 'none'",
        },
    },
    "/privacidade/": {
        "body": ("Versão 6", "portabilidade dos dados", "revogação do consentimento"),
        "headers": {"Referrer-Policy": "no-referrer"},
    },
    "/termos/": {
        "body": ("Versão 5", "relatório anual", "reconsideração"),
        "headers": {"Referrer-Policy": "no-referrer"},
    },
    "/docs/": {
        "body": ("Documentação Técnica",),
        "headers": {
            "Referrer-Policy": "no-referrer",
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "connect-src 'self'",
        },
    },
}

def unique_url(base: str, path: str) -> str:
    url = base.rstrip("/") + path
    parts = list(urllib.parse.urlsplit(url))
    query = urllib.parse.parse_qsl(parts[3], keep_blank_values=True)
    query.append(("__nocache", str(time.time_ns())))
    parts[3] = urllib.parse.urlencode(query)
    return urllib.parse.urlunsplit(parts)

def fetch(url: str):
    req = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": "daniel-site-production-validator/1.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        body = response.read().decode("utf-8", errors="replace")
        return response.geturl(), response.status, response.headers, body

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="https://daniel.fleck.dev.br")
    args = parser.parse_args()

    errors = []
    for path, rules in EXPECTED.items():
        url = unique_url(args.base_url, path)
        try:
            final_url, status, headers, body = fetch(url)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            errors.append(f"{path}: falha de acesso: {exc}")
            continue

        print(f"\n[{path}]")
        print("URL final:", final_url)
        print("Status:", status)
        for h in ("Date", "Age", "Via", "X-Cache", "X-Varnish", "Cache-Control", "ETag", "Last-Modified"):
            if headers.get(h):
                print(f"{h}: {headers.get(h)}")

        if status != 200:
            errors.append(f"{path}: status {status}")

        for fragment in rules["body"]:
            if fragment not in body:
                errors.append(f"{path}: conteúdo esperado ausente: {fragment!r}")

        for name, fragment in rules["headers"].items():
            value = headers.get(name, "")
            if fragment.lower() not in value.lower():
                errors.append(
                    f"{path}: header {name!r} não contém {fragment!r}; recebido={value!r}"
                )

        if path == "/docs/" and "api.github.com" in body.lower():
            errors.append("/docs/: referência inesperada a api.github.com no HTML inicial")

    if errors:
        print("\nVALIDAÇÃO DE PRODUÇÃO FALHOU")
        for err in errors:
            print("ERROR:", err)
        return 1

    print("\nVALIDAÇÃO DE PRODUÇÃO SEM CACHE: OK")
    print("Execute também:")
    print("python scripts/audit_network.py --base-url https://daniel.fleck.dev.br --all")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
