"""Gera um ZIP compacto do repositório para análise por uma IA.

O pacote exclui diretórios locais ou derivados que não ajudam na análise,
como ``.git``, ``.venv``, ``dist`` e ``__pycache__``. Também cria um índice
textual com a relação de arquivos incluídos.
"""

from __future__ import annotations

import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
AI_INDEX = DIST / "AI_INDEX.md"
ZIP_PATH = DIST / "site-for-ai.zip"
EXCLUDED_PARTS = {".git", ".venv", "dist", "__pycache__"}


def should_include(path: Path) -> bool:
    """Indica se um caminho deve fazer parte do pacote para IA."""

    relative = path.relative_to(ROOT)
    return path.is_file() and not any(
        part in EXCLUDED_PARTS for part in relative.parts
    )


def collect_files() -> list[Path]:
    """Retorna, em ordem estável, os arquivos relevantes do repositório."""

    return [path for path in sorted(ROOT.rglob("*")) if should_include(path)]


def build_index(files: list[Path]) -> str:
    """Monta o conteúdo do ``AI_INDEX.md`` incluído no ZIP."""

    items = "\n".join(f"- `{path.relative_to(ROOT)}`" for path in files)
    return (
        "# Pacote para análise por IA\n\n"
        "Forneça este ZIP a uma IA quando ela não conseguir varrer o "
        "repositório completo.\n\n"
        "## Arquivos\n\n"
        f"{items}\n"
    )


def main() -> int:
    """Cria ``dist/site-for-ai.zip`` e imprime o caminho resultante."""

    DIST.mkdir(exist_ok=True)
    files = collect_files()
    AI_INDEX.write_text(build_index(files), encoding="utf-8")

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT))

        # O índice é criado dentro de dist, que normalmente é excluído do
        # pacote; por isso ele é adicionado explicitamente ao final.
        archive.write(AI_INDEX, AI_INDEX.relative_to(ROOT))

    print(ZIP_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
