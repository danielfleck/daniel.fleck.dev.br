"""Validação estática do site, MkDocs, documentos legais e cabeçalhos.

Complemento dinâmico:
    python scripts/validate.py --network

Verificação do ambiente publicado:
    python scripts/validate.py --production-url https://daniel.fleck.dev.br
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

from site_utils import PROJECT_ROOT, SITE_ROOT, resolve_local_target, scan_content, tag_slug

DOCS_ROOT = SITE_ROOT / "docs"
MKDOCS_CONFIG = PROJECT_ROOT / "mkdocs" / "mkdocs.yml"
ROOT_HTACCESS = SITE_ROOT / ".htaccess"
DOCS_HTACCESS_SOURCE = PROJECT_ROOT / "mkdocs" / ".htaccess"
DOCS_HTACCESS_OUTPUT = DOCS_ROOT / ".htaccess"
SCRIPTS_SOURCE = PROJECT_ROOT / "SCRIPTS.md"
SCRIPTS_DOC = PROJECT_ROOT / "mkdocs" / "docs" / "desenvolvimento" / "scripts-python.md"

HOME = SITE_ROOT / "index.html"
PRE_COMMIT = PROJECT_ROOT / ".githooks" / "pre-commit"
PRE_PUSH = PROJECT_ROOT / ".githooks" / "pre-push"
GOVERNANCE_ROOT = PROJECT_ROOT / "mkdocs" / "docs" / "governanca"

HTML_ATTR_RE = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.I)
JSON_LD_RE = re.compile(
    r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
META_CSP_RE = re.compile(
    r'<meta[^>]+http-equiv=["\']Content-Security-Policy["\'][^>]*>',
    re.I,
)

AUTO_EXTERNAL_RE = [
    re.compile(r'<script[^>]+src=["\']https?://', re.I),
    re.compile(r'<img[^>]+src=["\']https?://', re.I),
    re.compile(r'<iframe[^>]+src=["\']https?://', re.I),
    re.compile(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']https?://', re.I),
    re.compile(r'<link[^>]+rel=["\']preconnect["\'][^>]+href=["\']https?://', re.I),
    re.compile(r'<link[^>]+rel=["\']dns-prefetch["\'][^>]+href=["\']https?://', re.I),
]

def public_html_files():
    docs_resolved = DOCS_ROOT.resolve()
    for path in SITE_ROOT.rglob("*.html"):
        try:
            path.resolve().relative_to(docs_resolved)
        except ValueError:
            yield path

def validate_content_metadata(errors: list[str], warnings: list[str]):
    try:
        items = scan_content(SITE_ROOT)
    except Exception as exc:
        errors.append(str(exc))
        return [], {}

    seen: set[tuple[str, str]] = set()
    tag_slugs: dict[str, str] = {}

    for item in items:
        key = (item.type, item.slug)
        if key in seen:
            errors.append(f"Duplicidade de conteúdo: {key}")
        seen.add(key)

        for field in ("title", "summary", "published", "display_date", "category"):
            if not getattr(item, field):
                errors.append(f"{item.path}: campo {field} vazio")

        if len(item.summary) > 280:
            warnings.append(
                f"{item.path.relative_to(SITE_ROOT)}: resumo longo "
                f"({len(item.summary)} caracteres)"
            )

        if not item.tags:
            errors.append(f"{item.path}: nenhuma tag")

        for tag in item.tags:
            slug = tag_slug(tag)
            previous = tag_slugs.get(slug)
            if previous and previous != tag:
                errors.append(f"Colisão de slug de tag: {previous!r} x {tag!r} -> {slug}")
            tag_slugs[slug] = tag

    return items, tag_slugs

def validate_html_pages(errors: list[str]) -> dict[str, Path]:
    canonicals: dict[str, Path] = {}

    for path in public_html_files():
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(SITE_ROOT)

        for pattern in AUTO_EXTERNAL_RE:
            if pattern.search(text):
                errors.append(f"Carregamento automático externo em {relative}")
                break

        if "data:image" in text.lower():
            errors.append(f"Imagem base64/data URI no site principal: {relative}")

        for csp_tag in META_CSP_RE.findall(text):
            if "frame-ancestors" in csp_tag.lower():
                errors.append(
                    f"{relative}: frame-ancestors não deve permanecer em CSP via <meta>; "
                    "use o cabeçalho HTTP do .htaccess."
                )

        if "showSection(" in text or 'onclick="showSection' in text:
            errors.append(f"Vestígio de SPA/showSection em {relative}")

        title = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
        h1 = re.search(r"<h1\b", text, re.I)
        desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)', text, re.I)
        canonical = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', text, re.I)

        if not title:
            errors.append(f"{relative}: <title> ausente")
        if not h1 and relative.name != "404.html":
            errors.append(f"{relative}: <h1> ausente")
        if not desc:
            errors.append(f"{relative}: meta description ausente")
        if canonical:
            url = canonical.group(1)
            if url in canonicals:
                errors.append(
                    f"Canonical duplicado: {url} em {relative} e "
                    f"{canonicals[url].relative_to(SITE_ROOT)}"
                )
            canonicals[url] = path
        elif relative.name != "404.html":
            errors.append(f"{relative}: canonical ausente")

        for block in JSON_LD_RE.findall(text):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{relative}: JSON-LD inválido: {exc}")

        for href in HTML_ATTR_RE.findall(text):
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:", "javascript:")):
                continue
            target = resolve_local_target(path, href)
            if target is not None and not target.exists():
                errors.append(f"{relative}: recurso/link local ausente: {href}")

    return canonicals

def validate_legal_documents(errors: list[str]) -> None:
    privacy = SITE_ROOT / "privacidade" / "index.html"
    terms = SITE_ROOT / "termos" / "index.html"

    for path in (privacy, terms):
        if not path.is_file():
            errors.append(f"Documento legal ausente: {path.relative_to(PROJECT_ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if "AI-LEGAL-MAINTENANCE" not in text:
            errors.append(f"{path.relative_to(PROJECT_ROOT)}: marcador legal ausente")

    if privacy.is_file():
        text = privacy.read_text(encoding="utf-8")
        for required in (
            "Versão 7",
            "localStorage",
            "sessionStorage",
            "Material for MkDocs",
            "connect-src",
        ):
            if required not in text:
                errors.append(f"Aviso de Privacidade V7 sem referência esperada: {required}")

    if terms.is_file():
        text = terms.read_text(encoding="utf-8")
        for required in ("Versão 6", "Web Storage", "/privacidade/", "Material for MkDocs"):
            if required not in text:
                errors.append(f"Termos V6 sem referência esperada: {required}")
        if 'href="#privacidade"' in text:
            errors.append("Termos ainda contêm link SPA antigo para #privacidade")

def validate_mkdocs_config(errors: list[str]) -> None:
    if not MKDOCS_CONFIG.is_file():
        errors.append("mkdocs/mkdocs.yml ausente")
        return

    text = MKDOCS_CONFIG.read_text(encoding="utf-8")
    forbidden = ("repo_url:", "repo_name:", "google_analytics:", "analytics:")
    for marker in forbidden:
        if re.search(rf"^\s*{re.escape(marker)}", text, re.M):
            errors.append(f"mkdocs.yml contém integração não permitida: {marker}")

    if not re.search(r"^\s*font:\s*false\s*$", text, re.M):
        errors.append("mkdocs.yml deve manter theme.font: false")

    if "Repositório no GitHub:" not in text:
        errors.append("mkdocs.yml deve manter o GitHub apenas como link normal de navegação")

def expected_scripts_doc() -> str:
    notice = """<!--
GENERATED FROM /SCRIPTS.md
NÃO EDITAR MANUALMENTE ESTA CÓPIA.
Execute: python scripts/build_docs.py
-->

"""
    return notice + SCRIPTS_SOURCE.read_text(encoding="utf-8")

def validate_scripts_mirror(errors: list[str]) -> None:
    if not SCRIPTS_SOURCE.is_file():
        errors.append("SCRIPTS.md ausente na raiz")
        return
    if not SCRIPTS_DOC.is_file():
        errors.append("Espelho MkDocs de SCRIPTS.md ausente")
        return
    if SCRIPTS_DOC.read_text(encoding="utf-8") != expected_scripts_doc():
        errors.append(
            "mkdocs/docs/desenvolvimento/scripts-python.md não corresponde a SCRIPTS.md; "
            "execute python scripts/build_docs.py"
        )

def validate_htaccess(errors: list[str]) -> None:
    required_root = {
        "Content-Security-Policy": "frame-ancestors 'none'",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "X-Content-Type-Options": "nosniff",
        "X-DNS-Prefetch-Control": "off",
    }

    if not ROOT_HTACCESS.is_file():
        errors.append("site/.htaccess ausente")
    else:
        text = ROOT_HTACCESS.read_text(encoding="utf-8")
        for header, value in required_root.items():
            if header not in text or value not in text:
                errors.append(f"site/.htaccess sem {header}: {value}")

    if not DOCS_HTACCESS_SOURCE.is_file():
        errors.append("mkdocs/.htaccess ausente")
        return

    docs_source = DOCS_HTACCESS_SOURCE.read_text(encoding="utf-8")
    for required in (
        "connect-src 'self'",
        "frame-ancestors 'none'",
        "script-src 'self' 'unsafe-inline'",
        "Referrer-Policy",
        "X-Frame-Options",
    ):
        if required not in docs_source:
            errors.append(f"mkdocs/.htaccess sem diretiva esperada: {required}")

    if not DOCS_HTACCESS_OUTPUT.is_file():
        errors.append("site/docs/.htaccess ausente; execute python scripts/build_docs.py")
    elif DOCS_HTACCESS_OUTPUT.read_text(encoding="utf-8") != docs_source:
        errors.append("site/docs/.htaccess difere de mkdocs/.htaccess")

def validate_home_legal_links(errors: list[str]) -> None:
    """Garante transparência jurídica mínima já na página inicial."""

    if not HOME.is_file():
        errors.append("site/index.html ausente")
        return

    text = HOME.read_text(encoding="utf-8")
    for href in ('href="/privacidade/"', 'href="/termos/"', 'href="/docs/"'):
        if href not in text:
            errors.append(f"Página inicial sem link obrigatório: {href}")

    if "Privacidade:" not in text:
        errors.append("Página inicial sem aviso resumido de privacidade no rodapé")

def validate_document_model(errors: list[str]) -> None:
    """Impede resumos de Confluence de voltarem para o MkDocs."""

    if not GOVERNANCE_ROOT.is_dir():
        errors.append("Pasta de governança MkDocs ausente")
        return

    summaries = sorted(GOVERNANCE_ROOT.rglob("*-resumo.md"))
    for path in summaries:
        errors.append(
            "Resumo indevido dentro do MkDocs; resumos pertencem ao Confluence: "
            f"{path.relative_to(PROJECT_ROOT)}"
        )

    required_current = {
        GOVERNANCE_ROOT / "index.md": (
            "Aviso de Privacidade: **Versão 7",
            "Termos de Uso: **Versão 6",
        ),
        GOVERNANCE_ROOT / "controle-versoes-documentos-legais.md": (
            "Aviso de Privacidade: Versão 7",
            "Termos de Uso: Versão 6",
        ),
        GOVERNANCE_ROOT / "registro-operacoes-tratamento.md": (
            "Web Storage funcional",
            "Aviso de Privacidade público **V7**",
            "Termos de Uso públicos **V6**",
        ),
        GOVERNANCE_ROOT / "due-diligence-kinghost.md": (
            "Header always set",
        ),
    }

    for path, fragments in required_current.items():
        if not path.is_file():
            errors.append(f"Documento de governança ausente: {path.relative_to(PROJECT_ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                errors.append(
                    f"{path.relative_to(PROJECT_ROOT)} sem referência atual esperada: {fragment}"
                )

def validate_hooks(errors: list[str]) -> None:
    """Confere que os hooks implementam o fluxo documentado."""

    if not PRE_COMMIT.is_file():
        errors.append(".githooks/pre-commit ausente")
    else:
        text = PRE_COMMIT.read_text(encoding="utf-8")
        for required in (
            "scripts/rebuild.py --hook",
            "scripts/build_docs.py --hook",
            "scripts/validate.py",
            "scripts/validate_docs.py",
        ):
            if required not in text:
                errors.append(f"pre-commit sem etapa esperada: {required}")

    if not PRE_PUSH.is_file():
        errors.append(".githooks/pre-push ausente")
    else:
        text = PRE_PUSH.read_text(encoding="utf-8")
        if "scripts/audit_network.py --all" not in text:
            errors.append("pre-push não executa audit_network.py --all")

def validate_mkdocs_navigation(errors: list[str]) -> None:
    """Confere itens críticos que precisam permanecer navegáveis."""

    if not MKDOCS_CONFIG.is_file():
        return

    text = MKDOCS_CONFIG.read_text(encoding="utf-8")
    required = (
        "governanca/index.md",
        "governanca/registro-operacoes-tratamento.md",
        "governanca/due-diligence-kinghost.md",
        "governanca/controle-versoes-documentos-legais.md",
        "seguranca/web-storage-mkdocs.md",
        "seguranca/csp-cabecalhos-http.md",
        "operacao/auditoria-rede-headless.md",
        "desenvolvimento/scripts-python.md",
        'Política de Privacidade: "https://daniel.fleck.dev.br/privacidade/"',
        'Termos de Uso: "https://daniel.fleck.dev.br/termos/"',
    )
    for item in required:
        if item not in text:
            errors.append(f"mkdocs.yml sem item crítico de navegação: {item}")


def validate_docs_output(errors: list[str]) -> None:
    for required in (DOCS_ROOT / "index.html", DOCS_ROOT / "sitemap.xml"):
        if not required.is_file():
            errors.append(f"Build MkDocs incompleto: {required.relative_to(PROJECT_ROOT)}")

    if DOCS_ROOT.exists():
        for path in DOCS_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if path.name == "mkdocs.yml" or path.suffix.lower() in {".md", ".py"}:
                errors.append(
                    "Arquivo-fonte indevido na saída pública MkDocs: "
                    f"{path.relative_to(PROJECT_ROOT)}"
                )
            if path.suffix.lower() == ".html":
                text = path.read_text(encoding="utf-8")
                for pattern in AUTO_EXTERNAL_RE:
                    if pattern.search(text):
                        errors.append(
                            "HTML MkDocs carrega recurso externo explicitamente: "
                            f"{path.relative_to(PROJECT_ROOT)}"
                        )
                        break

    process = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts/build_docs.py"), "--check"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        details = (process.stdout + process.stderr).strip()
        errors.append(
            "Documentação MkDocs desatualizada ou inválida. "
            "Execute python scripts/build_docs.py."
            + (f" Detalhes: {details}" if details else "")
        )

def validate_sitemap(errors: list[str], canonicals: dict[str, Path]) -> None:
    sitemap = SITE_ROOT / "sitemap.xml"
    if not sitemap.is_file():
        errors.append("site/sitemap.xml ausente")
        return
    try:
        tree = ET.parse(sitemap)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = [
            element.text
            for element in tree.findall(".//s:loc", ns)
            if element.text
        ]
        if len(locations) != len(set(locations)):
            errors.append("sitemap.xml possui URLs duplicadas")

        expected = set(canonicals)
        expected.discard("https://daniel.fleck.dev.br/404.html")
        missing = expected - set(locations)
        if missing:
            errors.append("sitemap.xml sem URLs canônicas: " + ", ".join(sorted(missing)))
    except Exception as exc:
        errors.append(f"sitemap.xml inválido: {exc}")

def validate_rebuild_state(errors: list[str]) -> None:
    process = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts/rebuild.py"), "--check"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        errors.append("Arquivos gerados estão desatualizados. Execute python scripts/rebuild.py.")

def header_value(headers, name: str) -> str:
    return headers.get(name, "")

def validate_production_headers(base_url: str, errors: list[str]) -> None:
    base = base_url.rstrip("/")
    checks = {
        "/": {
            "Content-Security-Policy": "frame-ancestors 'none'",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "no-referrer",
            "X-Content-Type-Options": "nosniff",
        },
        "/docs/": {
            "Content-Security-Policy": "connect-src 'self'",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "no-referrer",
            "X-Content-Type-Options": "nosniff",
        },
    }

    for path, required in checks.items():
        url = base + path
        request = urllib.request.Request(url, method="GET", headers={"User-Agent": "site-validator/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                headers = response.headers
                for name, fragment in required.items():
                    value = header_value(headers, name)
                    if fragment not in value:
                        errors.append(
                            f"{url}: header {name!r} não contém {fragment!r}; "
                            f"recebido={value!r}"
                        )
        except Exception as exc:
            errors.append(f"Falha ao validar headers de {url}: {exc}")

def run_network_audit(base_url: str | None, errors: list[str]) -> None:
    command = [sys.executable, str(PROJECT_ROOT / "scripts/audit_network.py"), "--all"]
    if base_url:
        command.extend(["--base-url", base_url.rstrip("/")])
    process = subprocess.run(command, cwd=PROJECT_ROOT)
    if process.returncode != 0:
        errors.append("Auditoria headless de rede falhou.")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", action="store_true", help="Executa também a auditoria headless.")
    parser.add_argument("--production-url", help="Valida headers HTTP do site já publicado.")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    items, tags = validate_content_metadata(errors, warnings)
    canonicals = validate_html_pages(errors)
    validate_legal_documents(errors)
    validate_mkdocs_config(errors)
    validate_mkdocs_navigation(errors)
    validate_scripts_mirror(errors)
    validate_home_legal_links(errors)
    validate_document_model(errors)
    validate_hooks(errors)
    validate_htaccess(errors)
    validate_docs_output(errors)
    validate_sitemap(errors, canonicals)
    validate_rebuild_state(errors)

    if args.production_url:
        validate_production_headers(args.production_url, errors)

    if args.network:
        run_network_audit(args.production_url, errors)

    if errors:
        print("VALIDAÇÃO FALHOU")
        for error in errors:
            print("ERROR:", error)
        for warning in warnings:
            print("WARN:", warning)
        return 1

    print(
        f"VALIDAÇÃO OK: {len(items)} conteúdos, {len(tags)} tags, "
        "documentos legais, MkDocs e controles de segurança consistentes."
    )
    for warning in warnings:
        print("WARN:", warning)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
