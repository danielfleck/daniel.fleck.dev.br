"""Funções compartilhadas pelos scripts de manutenção do site.

O site público fica em ``site/`` e usa arquivos HTML como fonte de
conteúdo. Cada página de blog, portfólio ou erro conhecido contém um bloco
``CONTENT-META`` que fornece os
metadados necessários para índices, tags, sitemap e SEO.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from html import escape
from pathlib import Path
from urllib.parse import unquote, urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT / "site"
TEMPLATES_ROOT = PROJECT_ROOT / "templates"
SCRIPTS_ROOT = PROJECT_ROOT / "scripts"

# Captura somente o bloco de metadados inserido nos arquivos de conteúdo.
# O modo DOTALL (re.S) permite que o bloco ocupe várias linhas.
META_RE = re.compile(r"<!--\s*CONTENT-META\s*(.*?)-->", re.S)


@dataclass(frozen=True)
class ContentMeta:
    """Metadados normalizados de uma página de conteúdo do site."""

    type: str
    slug: str
    title: str
    summary: str
    published: str
    display_date: str
    category: str
    status: str
    featured: bool
    tags: tuple[str, ...]
    path: Path

    @property
    def section(self) -> str:
        """Retorna a pasta pública correspondente ao tipo de conteúdo."""

        return {"blog": "blog", "portfolio": "portfolio", "error": "erros"}[
            self.type
        ]

    @property
    def url(self) -> str:
        """Retorna a URL pública relativa da página."""

        return f"/{self.section}/{self.slug}/"


def slugify(value: str) -> str:
    """Converte texto livre em slug ASCII seguro para uso em URLs.

    A conversão remove acentos, transforma letras em minúsculas e substitui
    sequências de caracteres não alfanuméricos por ``-``.
    """

    text = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "conteudo"


def parse_meta_text(text: str, path: Path) -> ContentMeta:
    """Extrai um bloco ``CONTENT-META`` e converte-o em ``ContentMeta``.

    O formato é deliberadamente simples: uma linha ``chave: valor`` por campo.
    Tags são separadas pelo caractere ``|`` para evitar a necessidade de um
    arquivo JSON ou YAML paralelo.
    """

    match = META_RE.search(text)
    if not match:
        raise ValueError(f"CONTENT-META ausente: {path}")

    values: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()

    tags = tuple(
        tag.strip() for tag in values.get("tags", "").split("|") if tag.strip()
    )

    return ContentMeta(
        type=values.get("type", ""),
        slug=values.get("slug", ""),
        title=values.get("title", ""),
        summary=values.get("summary", ""),
        published=values.get("published", ""),
        display_date=values.get("display_date", ""),
        category=values.get("category", ""),
        status=values.get("status", ""),
        featured=values.get("featured", "false").lower() == "true",
        tags=tags,
        path=path,
    )


def scan_content(root: Path = SITE_ROOT) -> list[ContentMeta]:
    """Varre blog, portfólio e erros conhecidos em busca de conteúdo.

    Apenas páginas no padrão ``<seção>/<slug>/index.html`` são consideradas
    conteúdo editorial. As páginas de índice das próprias seções não entram
    na lista.
    """

    items: list[ContentMeta] = []

    for section in ("blog", "portfolio", "erros"):
        base = root / section
        if not base.exists():
            continue

        for path in sorted(base.glob("*/index.html")):
            items.append(parse_meta_text(path.read_text(encoding="utf-8"), path))

    return items


def replace_region(text: str, name: str, inner: str) -> str:
    """Substitui somente o conteúdo de uma região ``GENERATED``.

    Os marcadores são mantidos no arquivo para que futuras execuções e outras
    ferramentas reconheçam claramente quais trechos são gerados e não devem
    ser editados manualmente.
    """

    start = f"<!-- GENERATED:{name}:START -->"
    end = f"<!-- GENERATED:{name}:END -->"

    if start not in text or end not in text:
        raise ValueError(f"Marcadores {name} ausentes")

    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return before + start + inner + end + after


def tag_slug(tag: str) -> str:
    """Converte o nome de uma tag no slug utilizado em ``/tags/<slug>/``."""

    return slugify(tag)


def html_tags(tags: tuple[str, ...] | list[str]) -> str:
    """Gera os links HTML correspondentes a uma coleção de tags."""

    return "".join(
        f'<a class="tag" href="/tags/{tag_slug(tag)}/">{escape(tag)}</a>'
        for tag in tags
    )


def resolve_local_target(
    page: Path,
    href: str,
    root: Path = SITE_ROOT,
) -> Path | None:
    """Resolve um ``href``/``src`` local para um caminho no sistema de arquivos.

    Referências externas, âncoras e esquemas como ``mailto:`` não apontam para
    arquivos locais e, por isso, retornam ``None``. A função é usada pelo
    validador para detectar links e recursos internos quebrados.
    """

    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None

    parsed = urlparse(href)
    if parsed.scheme in ("http", "https"):
        return None

    raw = unquote(parsed.path)
    if raw.startswith("/"):
        relative = raw.lstrip("/")
        target = root / relative
    else:
        target = (page.parent / raw).resolve()

    # URLs terminadas em / representam diretórios cuja página pública é
    # index.html. O segundo teste cobre diretórios já existentes sem barra.
    if raw.endswith("/") or target.is_dir():
        target = target / "index.html"

    return target
