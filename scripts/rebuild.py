"""Reconstrói os artefatos derivados dentro de ``site/``.

As páginas individuais em ``site/blog``, ``site/portfolio`` e ``site/erros``
são fontes de conteúdo.
Este script lê seus blocos ``CONTENT-META`` e atualiza automaticamente:

- navegação e rodapé compartilhados;
- SEO e cabeçalho das páginas de conteúdo;
- índices de blog, portfólio e erros;
- blocos dinâmicos da página inicial;
- nuvem e páginas individuais de tags;
- ``sitemap.xml`` e ``robots.txt``.

Regiões delimitadas por ``GENERATED:*`` não devem ser editadas manualmente,
pois serão sobrescritas na próxima execução deste script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from html import escape
from pathlib import Path

from site_config import AUTHOR, BASE_URL
from site_utils import (
    PROJECT_ROOT,
    SITE_ROOT,
    TEMPLATES_ROOT,
    html_tags,
    replace_region,
    scan_content,
    tag_slug,
)


NAV = (TEMPLATES_ROOT / "partials/nav.html").read_text(encoding="utf-8").strip()
FOOTER = (TEMPLATES_ROOT / "partials/footer.html").read_text(encoding="utf-8").strip()

# Páginas estáticas que compartilham os mesmos partials de navegação/rodapé.
STATIC_WITH_PARTIALS = [
    SITE_ROOT / "index.html",
    SITE_ROOT / "blog/index.html",
    SITE_ROOT / "portfolio/index.html",
    SITE_ROOT / "erros/index.html",
    SITE_ROOT / "roadmap/index.html",
    SITE_ROOT / "ferramentas/index.html",
    SITE_ROOT / "privacidade/index.html",
    SITE_ROOT / "termos/index.html",
    SITE_ROOT / "404.html",
]


# Assets públicos cujo conteúdo deve invalidar automaticamente caches antigos.
# O hash é calculado durante o rebuild; não existe número de versão manual.
VERSIONED_ASSETS = (
    "/css/base.css",
    "/css/layout.css",
    "/css/components.css",
    "/css/pages.css",
    "/js/main.js",
)


def asset_url(public_path: str) -> str:
    """Retorna URL do asset com versão derivada do próprio conteúdo.

    Exemplo:
        /css/components.css?v=ab12cd34ef56

    Se o arquivo mudar, o hash muda. Navegadores e proxies passam a enxergar
    uma URL diferente, evitando que uma versão antiga do CSS/JS continue ativa.
    """

    filesystem_path = SITE_ROOT / public_path.lstrip("/")
    digest = hashlib.sha256(filesystem_path.read_bytes()).hexdigest()[:12]
    return f"{public_path}?v={digest}"


def apply_asset_versions(text: str) -> str:
    """Atualiza referências a CSS/JS estáticos para seus hashes atuais."""

    for public_path in VERSIONED_ASSETS:
        versioned = asset_url(public_path)
        # Aceita tanto a referência sem query quanto uma versão gerada antes.
        pattern = re.escape(public_path) + r"(?:\?v=[0-9a-f]{12})?"
        text = re.sub(pattern, versioned, text)
    return text


class Writer:
    """Centraliza gravações e registra quais caminhos foram alterados.

    Quando ``write`` é falso, funciona como um dry-run: calcula as diferenças,
    mas não toca no sistema de arquivos. Esse comportamento sustenta a opção
    ``--check`` usada pelo validador e pelo hook de commit.
    """

    def __init__(self, write: bool = True) -> None:
        self.write = write
        self.changed: list[Path] = []

    def put(self, path: Path, text: str) -> None:
        """Grava ``text`` somente quando o conteúdo realmente mudou."""

        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old == text:
            return

        self.changed.append(path)
        if self.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")


def card(item) -> str:
    """Renderiza um card de listagem para qualquer tipo de conteúdo."""

    type_label = {
        "blog": "Blog",
        "portfolio": "Portfólio",
        "error": "Erro conhecido",
    }[item.type]

    meta = item.display_date
    if item.type == "error" and item.status:
        meta = f"{item.status} • {item.display_date}"

    return (
        f'<article class="card listing-card"><div class="type-label">'
        f"{escape(type_label)} • {escape(meta)}</div>"
        f'<h2><a href="{item.url}">{escape(item.title)}</a></h2>'
        f"<p>{escape(item.summary)}</p>"
        f'<div class="tag-row">{html_tags(item.tags)}</div>'
        f'<div class="project-links"><a class="project-link" '
        f'href="{item.url}">Abrir conteúdo</a></div></article>'
    )


def seo_block(item) -> str:
    """Gera title, description, canonical, Open Graph e JSON-LD da página."""

    schema = {
        "blog": "BlogPosting",
        "portfolio": "CreativeWork",
        "error": "TechArticle",
    }[item.type]
    url = BASE_URL + item.url

    data = {
        "@context": "https://schema.org",
        "@type": schema,
        "headline": item.title,
        "name": item.title,
        "description": item.summary,
        "url": url,
        "datePublished": item.published,
        "dateModified": item.published,
        "inLanguage": "pt-BR",
        "keywords": list(item.tags),
        "author": {
            "@type": "Person",
            "name": AUTHOR,
            "url": BASE_URL + "/",
        },
    }

    if item.type == "blog":
        data["articleSection"] = item.category
    if item.type == "error":
        data["articleSection"] = "Base de Conhecimento — Erros e Soluções"

    # Evita a sequência </ dentro do JSON-LD para não encerrar acidentalmente
    # a tag <script> caso algum dado futuro contenha esse padrão.
    json_ld = json.dumps(
        data,
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/")

    return (
        f"<title>{escape(item.title)} | Daniel Fleck</title>"
        f'<meta name="description" content="{escape(item.summary, quote=True)}">'
        f'<link rel="canonical" href="{url}">'
        '<meta property="og:type" content="article">'
        f'<meta property="og:title" content="{escape(item.title, quote=True)}">'
        f'<meta property="og:description" '
        f'content="{escape(item.summary, quote=True)}">'
        f'<meta property="og:url" content="{url}">'
        f'<script type="application/ld+json">{json_ld}</script>'
    )


def header_block(item) -> str:
    """Gera o cabeçalho editorial comum às páginas de conteúdo."""

    label = {
        "blog": item.category,
        "portfolio": "Portfólio",
        "error": "Erro conhecido",
    }[item.type]
    status = (
        f'<span class="tag success">{escape(item.status)}</span>'
        if item.status
        else ""
    )

    return (
        '<header class="page-header"><div class="article-meta">'
        f'<span class="tag brand">{escape(label)}</span>{status}'
        f'<span class="tag">{escape(item.display_date)}</span></div>'
        f"<h1>{escape(item.title)}</h1>"
        f'<p class="page-summary">{escape(item.summary)}</p>'
        f'<div class="tag-row">{html_tags(item.tags)}</div></header>'
    )


def links_block(item) -> str:
    """Gera as ações de retorno ao índice e de navegação por tags."""

    return (
        '<div class="content-actions"><a href="/'
        + item.section
        + '/">← Voltar ao índice</a><a href="/tags/">Explorar tags</a></div>'
    )


def tag_cloud(items) -> str:
    """Gera a nuvem de tags proporcional à frequência de uso."""

    frequencies = Counter(tag for item in items for tag in item.tags)
    if not frequencies:
        return '<div class="word-cloud"></div>'

    min_frequency = min(frequencies.values())
    max_frequency = max(frequencies.values())
    colors = ["blue", "teal", "orange", "muted"]
    parts: list[str] = []

    sorted_tags = sorted(
        frequencies.items(),
        key=lambda entry: (-entry[1], entry[0].casefold()),
    )

    for index, (tag, count) in enumerate(sorted_tags):
        ratio = (
            0.5
            if max_frequency == min_frequency
            else (count - min_frequency) / (max_frequency - min_frequency)
        )
        size = 11 + ratio * 9
        color = colors[index % len(colors)]
        parts.append(
            f'<a class="word-cloud-item {color}" '
            f'href="/tags/{tag_slug(tag)}/" '
            f'title="{escape(tag, quote=True)} — {count} ocorrência(s)" '
            f'style="font-size:{size:.1f}px">{escape(tag)}</a>'
        )

    return (
        '<div class="word-cloud" aria-label="Nuvem de tags">'
        + "".join(parts)
        + "</div>"
    )


def tag_page(tag: str, members) -> str:
    """Monta uma página estática que lista conteúdos de uma única tag."""

    groups = defaultdict(list)
    for item in members:
        groups[item.type].append(item)

    sections: list[str] = []
    labels = {
        "blog": "Blog",
        "portfolio": "Portfólio",
        "error": "Erros e soluções",
    }

    for content_type in ("blog", "portfolio", "error"):
        if groups[content_type]:
            ordered = sorted(
                groups[content_type],
                key=lambda item: item.published,
                reverse=True,
            )
            sections.append(
                f'<section class="tag-page-group"><h2>{labels[content_type]}</h2>'
                '<div class="listing-grid">'
                + "".join(card(item) for item in ordered)
                + "</div></section>"
            )

    url = f"{BASE_URL}/tags/{tag_slug(tag)}/"
    nav = (TEMPLATES_ROOT / "partials/nav.html").read_text(encoding="utf-8").strip()
    footer = (
        (TEMPLATES_ROOT / "partials/footer.html")
        .read_text(encoding="utf-8")
        .strip()
    )

    # A página gerada é intencionalmente autocontida no HTML. CSS/JS continuam
    # externos e estáticos, mas não há renderização de conteúdo no navegador.
    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="referrer" content="no-referrer">'
        '<meta http-equiv="Content-Security-Policy" '
        'content="default-src \'self\'; script-src \'self\'; style-src \'self\' '
        "'unsafe-inline'; img-src 'self'; font-src 'self'; connect-src 'self'; "
        "object-src 'none'; base-uri 'self'; form-action 'none'; "
        "frame-ancestors 'none'; upgrade-insecure-requests\">"
        f"<title>{escape(tag)} | Tags | Daniel Fleck</title>"
        f'<meta name="description" content="Conteúdos relacionados à tag '
        f'{escape(tag, quote=True)}.">'
        f'<link rel="canonical" href="{url}">'
        f'<link rel="stylesheet" href="{asset_url("/css/base.css")}">'
        f'<link rel="stylesheet" href="{asset_url("/css/layout.css")}">'
        f'<link rel="stylesheet" href="{asset_url("/css/components.css")}">'
        f'<link rel="stylesheet" href="{asset_url("/css/pages.css")}">'
        f'<script src="{asset_url("/js/main.js")}" defer></script></head><body>'
        '<!-- GENERATED-TAG-PAGE: não editar manualmente. ' 
        'Fonte: CONTENT-META das páginas. -->'
        f'{nav}<main class="container"><section class="section">'
        '<header class="page-header"><div class="section-kicker">Tag</div>'
        f"<h1>{escape(tag)}</h1>"
        f'<p class="page-summary">{len(members)} conteúdo(s) relacionado(s).</p>'
        f"</header>{''.join(sections)}</section></main>{footer}</body></html>"
    )


def tag_index(items) -> str:
    """Monta a página raiz ``/tags/`` com a nuvem de todas as tags."""

    nav = (TEMPLATES_ROOT / "partials/nav.html").read_text(encoding="utf-8").strip()
    footer = (
        (TEMPLATES_ROOT / "partials/footer.html")
        .read_text(encoding="utf-8")
        .strip()
    )
    cloud = tag_cloud(items)

    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="referrer" content="no-referrer">'
        '<meta http-equiv="Content-Security-Policy" '
        'content="default-src \'self\'; script-src \'self\'; style-src \'self\' '
        "'unsafe-inline'; img-src 'self'; font-src 'self'; connect-src 'self'; "
        "object-src 'none'; base-uri 'self'; form-action 'none'; "
        "frame-ancestors 'none'; upgrade-insecure-requests\">"
        "<title>Tags | Daniel Fleck</title>"
        '<meta name="description" content="Índice de tags do conteúdo técnico.">'
        f'<link rel="canonical" href="{BASE_URL}/tags/">'
        f'<link rel="stylesheet" href="{asset_url("/css/base.css")}">'
        f'<link rel="stylesheet" href="{asset_url("/css/layout.css")}">'
        f'<link rel="stylesheet" href="{asset_url("/css/components.css")}">'
        f'<link rel="stylesheet" href="{asset_url("/css/pages.css")}">'
        f'<script src="{asset_url("/js/main.js")}" defer></script></head><body>'
        '<!-- GENERATED-TAG-PAGE: não editar manualmente. -->'
        f'{nav}<main class="container"><section class="section">'
        '<header class="page-header"><div class="section-kicker">'
        "Descoberta de conteúdo</div><h1>Tags</h1>"
        '<p class="page-summary">A nuvem considera blog, portfólio e Base de '
        f"Conhecimento — Erros e Soluções.</p></header>{cloud}</section></main>"
        f"{footer}</body></html>"
    )


def apply_partials(text: str) -> str:
    """Atualiza navegação e rodapé quando os marcadores estiverem presentes."""

    if "<!-- GENERATED:SITE-NAV:START -->" in text:
        text = replace_region(text, "SITE-NAV", NAV)
    if "<!-- GENERATED:SITE-FOOTER:START -->" in text:
        text = replace_region(text, "SITE-FOOTER", FOOTER)
    return text


def build(write: bool = True) -> list[Path]:
    """Executa todo o processo de rebuild e retorna os caminhos alterados."""

    writer = Writer(write)
    items = scan_content(SITE_ROOT)

    # 1. Atualiza cada página editorial a partir de seus próprios metadados.
    for item in items:
        text = item.path.read_text(encoding="utf-8")
        text = apply_partials(text)
        text = replace_region(text, "SEO", seo_block(item))
        text = replace_region(text, "ARTICLE-HEADER", header_block(item))
        text = replace_region(text, "CONTENT-LINKS", links_block(item))
        text = apply_asset_versions(text)
        writer.put(item.path, text)

    # 2. Mantém partials compartilhados sincronizados nas páginas estáticas.
    for path in STATIC_WITH_PARTIALS:
        if path.exists():
            text = apply_partials(path.read_text(encoding="utf-8"))
            text = apply_asset_versions(text)
            writer.put(path, text)

    # 3. Reconstrói os índices principais por tipo de conteúdo.
    sorted_items = sorted(
        items,
        key=lambda item: (item.published, item.title),
        reverse=True,
    )
    by_type = {
        content_type: [item for item in sorted_items if item.type == content_type]
        for content_type in ("blog", "portfolio", "error")
    }

    index_specs = [
        (SITE_ROOT / "blog/index.html", "BLOG-LIST", by_type["blog"]),
        (SITE_ROOT / "portfolio/index.html", "PORTFOLIO-LIST", by_type["portfolio"]),
        (SITE_ROOT / "erros/index.html", "ERROS-LIST", by_type["error"]),
    ]

    for path, region, values in index_specs:
        text = path.read_text(encoding="utf-8")
        inner = (
            '<div class="listing-grid">'
            + "".join(card(item) for item in values)
            + "</div>"
        )
        text = replace_region(text, region, inner)
        text = apply_asset_versions(text)
        writer.put(path, text)

    # 4. Atualiza os blocos resumidos da página inicial.
    home = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
    featured = [item for item in by_type["portfolio"] if item.featured][:4]
    home = replace_region(
        home,
        "HOME-PORTFOLIO",
        '<div class="home-evidence-grid">'
        + "".join(card(item) for item in featured)
        + "</div>",
    )
    home = replace_region(
        home,
        "HOME-BLOG",
        '<div class="listing-grid">'
        + "".join(card(item) for item in by_type["blog"][:4])
        + "</div>",
    )
    home = replace_region(
        home,
        "HOME-ERRORS",
        '<div class="listing-grid">'
        + "".join(card(item) for item in by_type["error"][:3])
        + "</div>",
    )
    home = replace_region(home, "TAG-CLOUD", tag_cloud(items))
    home = apply_asset_versions(home)
    writer.put(SITE_ROOT / "index.html", home)

    # 5. Agrupa conteúdos por tag e remove páginas geradas que ficaram órfãs.
    tags = defaultdict(list)
    for item in items:
        for tag in item.tags:
            tags[tag].append(item)

    desired = {tag_slug(tag): tag for tag in tags}
    tags_root = SITE_ROOT / "tags"
    tags_root.mkdir(exist_ok=True)

    for child in tags_root.iterdir():
        tag_index_path = child / "index.html"
        if child.is_dir() and tag_index_path.exists():
            existing = tag_index_path.read_text(encoding="utf-8")
            if "GENERATED-TAG-PAGE" in existing and child.name not in desired:
                writer.changed.append(child)
                if write:
                    shutil.rmtree(child)

    for slug, tag in desired.items():
        writer.put(tags_root / slug / "index.html", tag_page(tag, tags[tag]))

    writer.put(tags_root / "index.html", tag_index(items))

    # 6. Gera sitemap e robots a partir das URLs públicas conhecidas.
    urls = [
        BASE_URL + "/",
        BASE_URL + "/curriculo.html",
        BASE_URL + "/blog/",
        BASE_URL + "/portfolio/",
        BASE_URL + "/erros/",
        BASE_URL + "/tags/",
        BASE_URL + "/roadmap/",
        BASE_URL + "/ferramentas/",
        BASE_URL + "/privacidade/",
        BASE_URL + "/termos/",
    ]
    urls += [BASE_URL + item.url for item in items]
    urls += [f"{BASE_URL}/tags/{slug}/" for slug in sorted(desired)]

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{escape(url)}</loc></url>\n" for url in urls)
        + "</urlset>\n"
    )
    writer.put(SITE_ROOT / "sitemap.xml", sitemap)

    robots = (
        f"User-agent: *\n"
        f"Allow: /\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
        f"Sitemap: {BASE_URL}/docs/sitemap.xml\n"
    )
    writer.put(SITE_ROOT / "robots.txt", robots)

    return writer.changed


def main() -> int:
    """Processa argumentos de linha de comando e executa o rebuild."""

    parser = argparse.ArgumentParser(
        description="Reconstrói os artefatos derivados do site estático."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Não grava; retorna código 2 se algum artefato estiver desatualizado.",
    )
    parser.add_argument(
        "--hook",
        action="store_true",
        help=(
            "Modo usado pelo hook Git; retorna código 3 se o rebuild "
            "alterar arquivos."
        ),
    )
    args = parser.parse_args()

    changed = build(write=not args.check)

    if changed:
        print("Arquivos que exigem rebuild/atualização:")
        for path in changed:
            print(" -", path.relative_to(PROJECT_ROOT))

        if args.check:
            return 2

        if args.hook:
            print(
                "\nO rebuild foi executado pelo hook e alterou arquivos gerados. "
                "Revise, faça git add e repita o commit."
            )
            return 3
    else:
        print("Rebuild: nenhum arquivo gerado precisou ser alterado.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
