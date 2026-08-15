#!/usr/bin/env python3
"""Verifica /stats e /varnish-stats sem autenticação, sem força bruta."""

from __future__ import annotations
import argparse
import urllib.error
import urllib.request

PATHS = ("/stats/", "/varnish-stats/")

def check(base: str, path: str) -> tuple[bool, str]:
    url = base.rstrip("/") + path
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "daniel-site-admin-surface-check/2.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            status = response.status
            if status == 200:
                return False, f"{path}: HTTP 200 sem credenciais ({response.geturl()})"
            return True, f"{path}: HTTP {status}"
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403, 404):
            return True, f"{path}: HTTP {exc.code} — conteúdo não exposto anonimamente"
        return False, f"{path}: HTTP {exc.code} inesperado"
    except urllib.error.URLError as exc:
        return False, f"{path}: não foi possível verificar: {exc}"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="https://daniel.fleck.dev.br")
    args = parser.parse_args()

    failures = 0
    for path in PATHS:
        ok, message = check(args.base_url, path)
        print(("OK: " if ok else "ALERTA: ") + message)
        failures += 0 if ok else 1
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
