"""Executa validações estruturais, de SEO e de integridade de ``site/``.

O validador foi pensado para rodar antes de commits e também manualmente. Ele
verifica metadados dos conteúdos, links locais, JSON-LD, canonical, sitemap,
recursos externos automáticos e se o rebuild está atualizado.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from site_utils import (
    PROJECT_ROOT,
    SITE_ROOT,
    resolve_local_target,
    scan_content,
    tag_slug,
)


HTML_ATTR_RE = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.I)
JSON_LD_RE = re.compile(
    r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)

# Carregamentos automáticos externos são proibidos pela arquitetura do site.
# Links comuns <a href="https://..."> continuam permitidos.

VERSIONED_PUBLIC_ASSETS = (
    "/css/base.css",
    "/css/layout.css",
    "/css/components.css",
    "/css/pages.css",
    "/js/main.js",
)


def expected_asset_url(public_path: str) -> str:
    """Calcula a URL versionada que deve aparecer nos HTMLs públicos."""

    path = SITE_ROOT / public_path.lstrip("/")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    return f"{public_path}?v={digest}"


AUTO_EXTERNAL_RE = [
    re.compile(r'<script[^>]+src=["\']https?://', re.I),
    re.compile(r'<img[^>]+src=["\']https?://', re.I),
    re.compile(r'<iframe[^>]+src=["\']https?://', re.I),
    re.compile(
        r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']https?://',
        re.I,
    ),
]



def public_html_files():
    """Itera somente pelos HTMLs dentro da raiz pública ``site/``."""

    yield from SITE_ROOT.rglob("*.html")


def validate_content_metadata(errors: list[str], warnings: list[str]):
    """Valida CONTENT-META e retorna conteúdos e mapa de slugs de tags."""

    try:
        items = scan_content(SITE_ROOT)
    except Exception as exc:  # noqa conceitual: erro precisa virar relatório.
        errors.append(str(exc))
        items = []

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

        if len(item.summary) > 220:
            warnings.append(
                f"{item.path.relative_to(SITE_ROOT)}: resumo longo "
                f"({len(item.summary)} caracteres)"
            )

        if not item.tags:
            errors.append(f"{item.path}: nenhuma tag")

        for tag in item.tags:
            slug = tag_slug(tag)
            if slug in tag_slugs and tag_slugs[slug] != tag:
                errors.append(
                    f"Colisão de slug de tag: {tag_slugs[slug]!r} x {tag!r} -> {slug}"
                )
            tag_slugs[slug] = tag

        page = item.path.read_text(encoding="utf-8")
        required_markers = (
            "CONTENT-META",
            "CONTENT-BODY:START",
            "CONTENT-BODY:END",
            "AI-CONTENT-MAINTENANCE",
        )
        for marker in required_markers:
            if marker not in page:
                errors.append(
                    f"{item.path.relative_to(SITE_ROOT)}: "
                    f"marcador/instrução ausente: {marker}"
                )

    return items, tag_slugs


def validate_html_pages(errors: list[str]) -> dict[str, Path]:
    """Valida páginas públicas e retorna ``canonical -> caminho``."""

    canonicals: dict[str, Path] = {}
    generated_indexes = {
        SITE_ROOT / "blog/index.html",
        SITE_ROOT / "portfolio/index.html",
        SITE_ROOT / "erros/index.html",
    }

    for path in public_html_files():
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(SITE_ROOT)

        if path in generated_indexes and "GENERATED:" not in text:
            errors.append(f"Marcadores de geração ausentes em {relative}")

        if re.search(r"\{\{[A-Z_]+\}\}", text):
            errors.append(f"Placeholder de template não resolvido: {relative}")

        if "<h1" not in text.lower():
            errors.append(f"H1 ausente: {relative}")

        if text.lower().count("<title>") != 1:
            errors.append(f"{relative}: esperado exatamente 1 <title>")

        canonical_matches = re.findall(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',
            text,
            re.I,
        )
        if len(canonical_matches) != 1:
            errors.append(
                f"{relative}: esperado exatamente 1 canonical; "
                f"encontrados {len(canonical_matches)}"
            )
        else:
            canonical = canonical_matches[0]
            if canonical in canonicals:
                errors.append(
                    f"Canonical duplicado: {relative} e {canonicals[canonical]} "
                    f"-> {canonical}"
                )
            canonicals[canonical] = relative

        descriptions = re.findall(
            r'<meta\s+name=["\']description["\']',
            text,
            re.I,
        )
        if len(descriptions) != 1:
            errors.append(f"{relative}: esperado exatamente 1 meta description")

        has_ai_instruction = (
            "AI-MAINTENANCE" in text
            or "AI-LEGAL-MAINTENANCE" in text
            or "GENERATED-TAG-PAGE" in text
        )
        if not has_ai_instruction:
            errors.append(f"{relative}: instrução de manutenção por IA ausente")

        for raw_json_ld in JSON_LD_RE.findall(text):
            try:
                json.loads(raw_json_ld)
            except Exception as exc:
                errors.append(f"JSON-LD inválido em {relative}: {exc}")

        # CSS/JS próprios precisam carregar uma versão baseada em hash.
        # Isso impede regressões em que o HTML continue apontando para um
        # stylesheet antigo armazenado em cache no navegador ou em proxy.
        for public_asset in VERSIONED_PUBLIC_ASSETS:
            if public_asset in text:
                expected = expected_asset_url(public_asset)
                if expected not in text:
                    errors.append(
                        f"Asset sem versão atual em {relative}: "
                        f"{public_asset} (esperado {expected})"
                    )

        for reference in HTML_ATTR_RE.findall(text):
            target = resolve_local_target(path, reference, SITE_ROOT)
            if target is None:
                continue

            # Depois da separação entre raiz do projeto e raiz pública, um
            # link relativo não pode escapar de site/. Caso contrário, ele
            # poderia existir no disco local (por exemplo README.md), mas não
            # estaria disponível quando somente site/ fosse publicado.
            try:
                target.resolve().relative_to(SITE_ROOT.resolve())
            except ValueError:
                errors.append(
                    f"Link/recurso sai da raiz pública: {relative} -> {reference}"
                )
                continue

            if not target.exists():
                errors.append(
                    f"Link/recurso local inexistente: {relative} -> {reference}"
                )

        if any(regex.search(text) for regex in AUTO_EXTERNAL_RE):
            errors.append(f"Recurso externo automático: {relative}")

        if "data:image" in text.lower():
            errors.append(f"Imagem base64/data URI: {relative}")

    return canonicals


def validate_sitemap(errors: list[str], canonicals: dict[str, Path]) -> None:
    """Compara as URLs do sitemap com o conjunto de URLs canônicas."""

    try:
        tree = ET.parse(SITE_ROOT / "sitemap.xml")
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = [
            element.text
            for element in tree.findall(".//s:loc", namespace)
            if element.text
        ]

        if len(locations) != len(set(locations)):
            errors.append("sitemap.xml possui URLs duplicadas")

        expected = set(canonicals)
        # A página 404 é pública para o servidor, mas não deve ser indexada.
        expected.discard("https://daniel.fleck.dev.br/404.html")

        missing = expected - set(locations)
        extra = set(locations) - expected

        if missing:
            errors.append(
                "sitemap.xml sem URLs canônicas: " + ", ".join(sorted(missing))
            )
        if extra:
            errors.append(
                "sitemap.xml possui URLs sem página canônica correspondente: "
                + ", ".join(sorted(extra))
            )
    except Exception as exc:
        errors.append(f"sitemap.xml inválido: {exc}")


def validate_rebuild_state(errors: list[str]) -> None:
    """Confirma que uma nova execução do rebuild não produziria alterações."""

    process = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts/rebuild.py"), "--check"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        errors.append(
            "Arquivos gerados estão desatualizados. Execute python scripts/rebuild.py."
        )


def main() -> int:
    """Executa todas as validações e retorna código adequado ao shell/Git."""

    errors: list[str] = []
    warnings: list[str] = []

    items, tag_slugs = validate_content_metadata(errors, warnings)
    canonicals = validate_html_pages(errors)
    validate_sitemap(errors, canonicals)
    validate_rebuild_state(errors)

    if errors:
        print("VALIDAÇÃO FALHOU")
        for error in errors:
            print("ERROR:", error)
        for warning in warnings:
            print("WARN:", warning)
        return 1

    print(
        f"VALIDAÇÃO OK: {len(items)} conteúdos, {len(tag_slugs)} tags e "
        "links/SEO locais consistentes."
    )
    for warning in warnings:
        print("WARN:", warning)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
