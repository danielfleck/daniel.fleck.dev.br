"""Cria uma nova página de blog, portfólio ou erro conhecido.

O script usa templates HTML e grava os metadados no próprio arquivo gerado.
Depois da criação, executa o rebuild para atualizar índices, tags e sitemap.
O corpo editorial permanece para edição manual entre os marcadores
``CONTENT-BODY:START`` e ``CONTENT-BODY:END``.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date

from site_utils import ROOT, slugify


TYPE_MAP = {
    "blog": ("blog", "blog.html"),
    "portfolio": ("portfolio", "portfolio.html"),
    "erro": ("erros", "erro.html"),
}

MONTHS = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
]


def display_date(iso_date: str) -> str:
    """Converte ``AAAA-MM-DD`` para a forma curta usada na interface."""

    year, month, day = iso_date.split("-")
    return f"{day} {MONTHS[int(month) - 1]} {year}"


def ask(label: str, default: str = "") -> str:
    """Solicita um valor no terminal e aceita um padrão opcional."""

    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def validate_inline_metadata(values: list[str]) -> None:
    """Impede caracteres que quebrariam o bloco de comentário CONTENT-META."""

    if any("\n" in value or "\r" in value or "-->" in value for value in values):
        raise SystemExit(
            "Metadados não podem conter quebra de linha nem a sequência -->."
        )


def run_rebuild() -> None:
    """Reconstrói os artefatos derivados após criar a nova página."""

    subprocess.run(
        [sys.executable, str(ROOT / "scripts/rebuild.py")],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    """Executa o assistente interativo de criação de conteúdo."""

    parser = argparse.ArgumentParser(
        description="Cria conteúdo estático a partir de um template."
    )
    parser.add_argument("tipo", choices=TYPE_MAP)
    args = parser.parse_args()

    section, template_name = TYPE_MAP[args.tipo]

    title = ask("Título")
    if not title:
        raise SystemExit("Título obrigatório.")

    summary = ask("Resumo")
    if not summary:
        raise SystemExit("Resumo obrigatório.")

    published = ask("Data ISO (AAAA-MM-DD)", date.today().isoformat())
    try:
        date.fromisoformat(published)
    except ValueError as exc:
        raise SystemExit(
            "Data inválida. Use AAAA-MM-DD, por exemplo 2026-08-10."
        ) from exc

    slug = slugify(ask("Slug", slugify(title)))
    category = ask(
        "Categoria",
        {
            "blog": "Técnico",
            "portfolio": "Portfólio",
            "erro": "Troubleshooting",
        }[args.tipo],
    )
    status = ask("Status", "Resolvido") if args.tipo == "erro" else ""

    raw_tags = ask("Tags separadas por vírgula")
    tag_values = [tag.strip() for tag in raw_tags.split(",") if tag.strip()]
    if not tag_values:
        raise SystemExit("Informe pelo menos uma tag.")

    validate_inline_metadata([title, summary, category, status, *tag_values])

    target = ROOT / section / slug / "index.html"
    if target.exists():
        raise SystemExit(f"Slug já existe: {target.relative_to(ROOT)}")

    template = (ROOT / "templates" / template_name).read_text(encoding="utf-8")

    featured = "false"
    if args.tipo == "portfolio":
        answer = ask("Destacar na página inicial? (s/n)", "n").lower()
        featured = "true" if answer in {"s", "sim", "y", "yes"} else "false"

    replacements = {
        "{{TITLE}}": title,
        "{{SUMMARY}}": summary,
        "{{PUBLISHED}}": published,
        "{{DISPLAY_DATE}}": display_date(published),
        "{{SLUG}}": slug,
        "{{CATEGORY}}": category,
        "{{STATUS}}": status,
        "{{FEATURED}}": featured,
        "{{TAGS}}": " | ".join(tag_values),
    }

    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(template, encoding="utf-8")
    print("Criado:", target.relative_to(ROOT))

    run_rebuild()
    print(
        "Edite somente o corpo entre CONTENT-BODY:START e CONTENT-BODY:END "
        "e execute novamente python scripts/rebuild.py."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
