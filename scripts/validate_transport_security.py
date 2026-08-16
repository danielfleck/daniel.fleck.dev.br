#!/usr/bin/env python3
"""Valida HTTP→HTTPS, HSTS e security.txt.

Sem argumentos: valida arquivos locais.
Com --production-url: valida também a produção.
"""

from __future__ import annotations
import argparse
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
HTACCESS = SITE / ".htaccess"
SECURITY_TXT = SITE / ".well-known" / "security.txt"
SECURITY_PAGE = SITE / "seguranca" / "index.html"
REBUILD = ROOT / "scripts" / "rebuild.py"
MIN_HSTS = 31_536_000

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def local_errors(allow_test_stage=False):
    errors = []
    for path in (HTACCESS, SECURITY_TXT, SECURITY_PAGE):
        if not path.is_file():
            errors.append(f"arquivo ausente: {path.relative_to(ROOT)}")

    if SECURITY_PAGE.is_file():
        page = SECURITY_PAGE.read_text(encoding="utf-8")
        for number in range(1, 9):
            marker = f"SECURITY-RATIONALE:{number:02d}"
            if marker not in page:
                errors.append(f"site/seguranca/index.html sem {marker}")

    if HTACCESS.is_file():
        text = HTACCESS.read_text(encoding="utf-8")
        if "RewriteEngine On" not in text:
            errors.append("site/.htaccess sem RewriteEngine On")
        if "https://daniel.fleck.dev.br" not in text:
            errors.append("site/.htaccess sem destino HTTPS canônico")
        m = re.search(r'Strict-Transport-Security\s+"[^"]*max-age=(\d+)', text, re.I)
        if not m:
            errors.append("HSTS ausente em site/.htaccess")
        elif int(m.group(1)) < MIN_HSTS:
            value = int(m.group(1))
            if allow_test_stage and value >= 300 and "[R=302" in text:
                print(
                    "TRANSPORTE/SEGURANÇA: fase de teste detectada "
                    f"(302 + HSTS max-age={value})."
                )
            else:
                errors.append(f"HSTS final exige max-age >= {MIN_HSTS}")

    if SECURITY_TXT.is_file():
        text = SECURITY_TXT.read_text(encoding="utf-8")
        fields = {}
        for raw in text.splitlines():
            raw = raw.strip()
            if not raw or raw.startswith("#") or ":" not in raw:
                continue
            key, value = raw.split(":", 1)
            fields.setdefault(key.strip().lower(), []).append(value.strip())

        if not fields.get("contact"):
            errors.append("security.txt sem Contact")
        if len(fields.get("expires", [])) != 1:
            errors.append("security.txt deve ter exatamente um Expires")
        expected = "https://daniel.fleck.dev.br/.well-known/security.txt"
        if fields.get("canonical", [""])[0] != expected:
            errors.append("security.txt sem Canonical esperado")
        if fields.get("expires"):
            try:
                expires = datetime.fromisoformat(fields["expires"][0].replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                if expires <= now:
                    errors.append("security.txt expirado")
                if (expires - now).days >= 366:
                    errors.append("Expires deveria ficar a menos de um ano")
            except ValueError:
                errors.append("Expires inválido")

    if REBUILD.is_file():
        text = REBUILD.read_text(encoding="utf-8")
        if 'SITE_ROOT / "seguranca/index.html"' not in text:
            errors.append("rebuild.py sem seguranca/index.html em STATIC_WITH_PARTIALS")
        if 'BASE_URL + "/seguranca/"' not in text:
            errors.append("rebuild.py sem /seguranca/ no sitemap")
    return errors

def no_redirect_get(url):
    opener = urllib.request.build_opener(
        NoRedirect(), urllib.request.HTTPSHandler(context=ssl.create_default_context())
    )
    req = urllib.request.Request(url, headers={
        "User-Agent": "daniel-site-transport-validator/1.0",
        "Cache-Control": "no-cache, no-store, max-age=0",
        "Pragma": "no-cache",
    })
    try:
        r = opener.open(req, timeout=20)
        return r.status, r.headers, r.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers, exc.read()

def follow_get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "daniel-site-transport-validator/1.0",
        "Cache-Control": "no-cache, no-store, max-age=0",
        "Pragma": "no-cache",
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status, r.headers, r.read()

def production_errors(base_https):
    errors = []
    parsed = urllib.parse.urlsplit(base_https)
    host = parsed.netloc
    https_origin = f"https://{host}"
    http_origin = f"http://{host}"

    paths = (
        "/", "/docs/", "/privacidade/", "/termos/",
        "/.well-known/security.txt", "/blog/?transport_test=1",
    )
    for path in paths:
        status, headers, _ = no_redirect_get(http_origin + path)
        expected = https_origin + path
        if status not in (301, 308):
            errors.append(f"HTTP {path}: esperado 301/308, recebido {status}")
        if headers.get("Location", "") != expected:
            errors.append(
                f"HTTP {path}: Location esperado {expected!r}, "
                f"recebido {headers.get('Location', '')!r}"
            )

    for secure_path in ("/", "/docs/"):
        status, headers, _ = follow_get(https_origin + secure_path)
        if status != 200:
            errors.append(
                f"HTTPS {secure_path}: esperado 200, recebido {status}"
            )
            continue
        hsts = headers.get("Strict-Transport-Security", "")
        m = re.search(r"(?:^|;)\s*max-age=(\d+)", hsts, re.I)
        if not m:
            errors.append(
                f"produção HTTPS {secure_path} sem HSTS/max-age"
            )
        elif int(m.group(1)) < MIN_HSTS:
            errors.append(
                f"HSTS em {secure_path} abaixo de {MIN_HSTS}"
            )

    status, headers, body = follow_get(https_origin + "/.well-known/security.txt")
    if status != 200:
        errors.append(f"security.txt: esperado 200, recebido {status}")
    if "text/plain" not in headers.get("Content-Type", "").lower():
        errors.append("security.txt deveria ser servido como text/plain")
    text = body.decode("utf-8", errors="replace")
    for field in ("Contact:", "Expires:", "Canonical:", "Policy:"):
        if field not in text:
            errors.append(f"security.txt publicado sem {field}")

    expires_match = re.search(r"^Expires:\s*(\S+)\s*$", text, re.M)
    if expires_match:
        try:
            expires = datetime.fromisoformat(
                expires_match.group(1).replace("Z", "+00:00")
            )
            if expires <= datetime.now(timezone.utc):
                errors.append("security.txt publicado está expirado")
        except ValueError:
            errors.append("security.txt publicado possui Expires inválido")

    status, _, _ = follow_get(https_origin + "/seguranca/")
    if status != 200:
        errors.append(f"/seguranca/: esperado 200, recebido {status}")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--production-url")
    parser.add_argument(
        "--allow-test-stage",
        action="store_true",
        help="Aceita temporariamente 302 + HSTS max-age>=300 na validação local.",
    )
    args = parser.parse_args()
    errors = local_errors(allow_test_stage=args.allow_test_stage)
    if args.production_url:
        if not args.production_url.startswith("https://"):
            errors.append("--production-url deve usar https://")
        else:
            try:
                errors.extend(production_errors(args.production_url))
            except Exception as exc:
                errors.append(f"falha na produção: {exc}")

    if errors:
        print("TRANSPORTE/SEGURANÇA: FALHOU")
        for error in errors:
            print("ERROR:", error)
        return 1
    print("TRANSPORTE/SEGURANÇA: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
