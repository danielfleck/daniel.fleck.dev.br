#!/usr/bin/env python3
"""Verifica /stats e /varnish-stats sem autenticação e sem força bruta."""

from __future__ import annotations

import argparse
import urllib.error
import urllib.request


PATHS = ("/stats/", "/varnish-stats/")


def check(base: str, path: str) -> tuple[str, str]:
    url = base.rstrip("/") + path

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "daniel-site-admin-surface-check/3.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            status = response.status
            final_url = response.geturl()

            if status == 200:
                if path == "/stats/":
                    return (
                        "WARN",
                        f"{path}: HTTP 200 sem credenciais ({final_url}) — "
                        "superfície pública conhecida da hospedagem KingHost; "
                        "não bloqueia a validação.",
                    )

                return (
                    "ERROR",
                    f"{path}: HTTP 200 sem credenciais ({final_url})",
                )

            return "OK", f"{path}: HTTP {status}"

    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403, 404):
            return (
                "OK",
                f"{path}: HTTP {exc.code} — conteúdo não exposto anonimamente",
            )

        return "ERROR", f"{path}: HTTP {exc.code} inesperado"

    except urllib.error.URLError as exc:
        return "ERROR", f"{path}: não foi possível verificar: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        default="https://daniel.fleck.dev.br",
    )
    args = parser.parse_args()

    failures = 0

    for path in PATHS:
        level, message = check(args.base_url, path)
        print(f"{level}: {message}")

        if level == "ERROR":
            failures += 1

    if failures:
        print("CHECK ADMIN SURFACES: FALHOU")
        return 1

    print("CHECK ADMIN SURFACES: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
