"""Remove frame-ancestors de CSPs entregues por <meta>.

A proteção passa a ser entregue por cabeçalho HTTP em site/.htaccess
e site/docs/.htaccess.

O script também corrige o gerador de páginas de tags para não reintroduzir
frame-ancestors nas próximas execuções de rebuild.py.
"""

from __future__ import annotations

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT / "site"
TEMPLATES = PROJECT_ROOT / "templates"
REBUILD = PROJECT_ROOT / "scripts" / "rebuild.py"

META_CSP_RE = re.compile(
    r'<meta[^>]+http-equiv=["\']Content-Security-Policy["\'][^>]*>',
    re.I,
)
FRAME_RE = re.compile(r"\s*frame-ancestors\s+'none'\s*;\s*", re.I)


def clean_meta_text(text: str) -> str:
    def replace_tag(match: re.Match[str]) -> str:
        return FRAME_RE.sub(" ", match.group(0))

    return META_CSP_RE.sub(replace_tag, text)


def update_file(path: Path, transform) -> bool:
    old = path.read_text(encoding="utf-8")
    new = transform(old)
    if old == new:
        return False

    path.write_text(new, encoding="utf-8")
    print("Atualizado:", path.relative_to(PROJECT_ROOT))
    return True


def main() -> int:
    changed = 0

    for path in sorted(SITE_ROOT.rglob("*.html")):
        try:
            path.relative_to(SITE_ROOT / "docs")
            continue
        except ValueError:
            pass

        changed += int(update_file(path, clean_meta_text))

    for path in sorted(TEMPLATES.rglob("*.html")):
        changed += int(update_file(path, clean_meta_text))

    if REBUILD.is_file():
        def clean_rebuild(text: str) -> str:
            # O gerador atual contém a diretiva em literais HTML.
            # Removemos somente a sequência CSP conhecida.
            return text.replace("frame-ancestors 'none'; ", "")

        changed += int(update_file(REBUILD, clean_rebuild))

    print(f"Concluído. Arquivos alterados: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
