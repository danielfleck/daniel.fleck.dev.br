"""Gera a documentação MkDocs em ``site/docs/``.

O Markdown-fonte permanece fora da raiz pública, em ``mkdocs/docs/``.
Somente o HTML/CSS/JS gerado pelo MkDocs é gravado em ``site/docs/``.

Modos:
- padrão: executa o build e grava a saída;
- --check: gera em diretório temporário e compara com ``site/docs``;
- --hook: grava normalmente e retorna 3 se o build alterou a saída versionada.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG = PROJECT_ROOT / "mkdocs" / "mkdocs.yml"
OUTPUT = PROJECT_ROOT / "site" / "docs"


def snapshot(root: Path) -> dict[str, str]:
    """Retorna hashes estáveis de todos os arquivos existentes em ``root``."""

    if not root.exists():
        return {}

    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def normalize_sitemap_gzip(root: Path) -> None:
    """Regrava sitemap.xml.gz com ``mtime=0`` para build determinístico."""

    xml = root / "sitemap.xml"
    gz = root / "sitemap.xml.gz"
    if not xml.exists():
        return

    gz.write_bytes(gzip.compress(xml.read_bytes(), mtime=0))


def run_mkdocs(destination: Path) -> None:
    """Executa o MkDocs em modo estrito para ``destination``."""

    command = [
        sys.executable,
        "-m",
        "mkdocs",
        "build",
        "--config-file",
        str(CONFIG),
        "--site-dir",
        str(destination),
        "--clean",
        "--strict",
    ]

    try:
        process = subprocess.run(command, cwd=PROJECT_ROOT)
    except FileNotFoundError as exc:
        raise RuntimeError(
            "MkDocs não encontrado. Ative a .venv e execute "
            "`python -m pip install -e .`."
        ) from exc

    if process.returncode != 0:
        raise RuntimeError("mkdocs build falhou.")

    normalize_sitemap_gzip(destination)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera e confere a documentação técnica MkDocs."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compara um build temporário com site/docs sem alterar arquivos.",
    )
    parser.add_argument(
        "--hook",
        action="store_true",
        help="Retorna 3 quando o build do hook modificar site/docs.",
    )
    args = parser.parse_args()

    if not CONFIG.exists():
        print(f"Configuração MkDocs não encontrada: {CONFIG}")
        return 1

    if args.check:
        with tempfile.TemporaryDirectory(prefix="mkdocs-check-") as temporary:
            temp_output = Path(temporary) / "site"
            try:
                run_mkdocs(temp_output)
            except RuntimeError as exc:
                print(exc)
                return 1

            if snapshot(temp_output) != snapshot(OUTPUT):
                print(
                    "Documentação gerada está desatualizada. "
                    "Execute: python scripts/build_docs.py"
                )
                return 2

        print("MkDocs: site/docs está atualizado.")
        return 0

    before = snapshot(OUTPUT)

    try:
        run_mkdocs(OUTPUT)
    except RuntimeError as exc:
        print(exc)
        return 1

    after = snapshot(OUTPUT)

    if before != after:
        print("MkDocs: site/docs foi atualizado.")
        if args.hook:
            print(
                "Commit interrompido: o build da documentação alterou "
                "arquivos em site/docs. Revise, faça git add -A e repita."
            )
            return 3
    else:
        print("MkDocs: nenhum arquivo precisou ser alterado.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
