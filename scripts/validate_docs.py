"""Validação específica da saída pública Material for MkDocs."""

from __future__ import annotations

import argparse
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT / "site"
DOCS_ROOT = SITE_ROOT / "docs"
DOCS_HTACCESS_SOURCE = PROJECT_ROOT / "mkdocs" / ".htaccess"
DOCS_HTACCESS_OUTPUT = DOCS_ROOT / ".htaccess"

AUTO_EXTERNAL_RE = [
    re.compile(r'<script[^>]+src=["\']https?://', re.I),
    re.compile(r'<img[^>]+src=["\']https?://', re.I),
    re.compile(r'<iframe[^>]+src=["\']https?://', re.I),
    re.compile(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']https?://', re.I),
    re.compile(r'<link[^>]+href=["\']https://fonts\.', re.I),
]
HTML_LINK_RE = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.I)
CSS_EXTERNAL_RE = re.compile(r'url\(\s*["\']?https?://', re.I)

def resolve_local(page: Path, raw: str) -> Path | None:
    if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "blob:")):
        return None
    parsed = urlsplit(raw)
    if parsed.scheme in {"http", "https"} or parsed.netloc:
        return None
    path = parsed.path
    if not path:
        return None
    target = SITE_ROOT / path.lstrip("/") if path.startswith("/") else page.parent / path
    if path.endswith("/"):
        target = target / "index.html"
    elif target.is_dir():
        target = target / "index.html"
    return target

def validate_output() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for path in (DOCS_ROOT / "index.html", DOCS_ROOT / "sitemap.xml"):
        if not path.is_file():
            errors.append(f"Arquivo obrigatório ausente: {path.relative_to(PROJECT_ROOT)}")

    if not DOCS_HTACCESS_SOURCE.is_file():
        errors.append("mkdocs/.htaccess ausente")
    elif not DOCS_HTACCESS_OUTPUT.is_file():
        errors.append("site/docs/.htaccess ausente; execute python scripts/build_docs.py")
    elif DOCS_HTACCESS_SOURCE.read_text(encoding="utf-8") != DOCS_HTACCESS_OUTPUT.read_text(encoding="utf-8"):
        errors.append("site/docs/.htaccess difere de mkdocs/.htaccess")

    if not DOCS_ROOT.exists():
        return errors, warnings

    for path in DOCS_ROOT.rglob("*"):
        if not path.is_file():
            continue

        relative = path.relative_to(PROJECT_ROOT)

        if path.name == "mkdocs.yml" or path.suffix.lower() in {".md", ".py"}:
            errors.append(f"Fonte indevida na saída pública MkDocs: {relative}")

        if path.suffix.lower() == ".css":
            text = path.read_text(encoding="utf-8", errors="ignore")
            if CSS_EXTERNAL_RE.search(text):
                errors.append(f"CSS do MkDocs carrega URL externa automaticamente: {relative}")

        if path.suffix.lower() != ".html":
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(regex.search(text) for regex in AUTO_EXTERNAL_RE):
            errors.append(f"Recurso externo automático no MkDocs: {relative}")

        for reference in HTML_LINK_RE.findall(text):
            target = resolve_local(path, reference)
            if target is None:
                continue
            try:
                target.resolve().relative_to(SITE_ROOT.resolve())
            except ValueError:
                errors.append(f"Referência sai da raiz pública: {relative} -> {reference}")
                continue
            if not target.exists():
                errors.append(f"Link/recurso local inexistente: {relative} -> {reference}")

    sitemap = DOCS_ROOT / "sitemap.xml"
    if sitemap.exists():
        try:
            tree = ET.parse(sitemap)
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            urls = [el.text for el in tree.findall(".//s:loc", ns) if el.text]
            if len(urls) != len(set(urls)):
                errors.append("site/docs/sitemap.xml possui URLs duplicadas")
            for url in urls:
                if not url.startswith("https://daniel.fleck.dev.br/docs/"):
                    errors.append(f"URL inesperada no sitemap do MkDocs: {url}")
        except Exception as exc:
            errors.append(f"site/docs/sitemap.xml inválido: {exc}")

    if any(
        "<script>" in p.read_text(encoding="utf-8", errors="ignore")
        for p in DOCS_ROOT.rglob("*.html")
    ):
        warnings.append(
            "MkDocs contém JavaScript inline; a exceção de script-src em /docs/ "
            "deve permanecer limitada à documentação e ser reavaliada se o tema mudar."
        )

    return errors, warnings

def check_production_headers(url: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    request = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": "site-validator/2.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            headers = response.headers
    except (urllib.error.URLError, TimeoutError) as exc:
        return [f"Não foi possível consultar {url}: {exc}"], warnings

    required = {
        "Content-Security-Policy": (
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "script-src 'self' 'unsafe-inline'",
        ),
        "X-Frame-Options": ("DENY",),
        "Referrer-Policy": ("no-referrer",),
        "X-Content-Type-Options": ("nosniff",),
    }

    for name, fragments in required.items():
        value = headers.get(name, "")
        for fragment in fragments:
            if fragment.lower() not in value.lower():
                errors.append(
                    f"{url}: header {name!r} não contém {fragment!r}; recebido={value!r}"
                )

    return errors, warnings

def main() -> int:
    parser = argparse.ArgumentParser(description="Valida a documentação MkDocs.")
    parser.add_argument(
        "--production-url",
        help="URL de /docs/ publicada, por exemplo https://daniel.fleck.dev.br/docs/",
    )
    args = parser.parse_args()

    errors, warnings = validate_output()
    if args.production_url:
        extra_errors, extra_warnings = check_production_headers(args.production_url)
        errors.extend(extra_errors)
        warnings.extend(extra_warnings)

    if errors:
        print("VALIDAÇÃO MKDOCS FALHOU")
        for item in errors:
            print("ERROR:", item)
        for item in warnings:
            print("WARN:", item)
        return 1

    print("VALIDAÇÃO MKDOCS OK")
    for item in warnings:
        print("WARN:", item)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
