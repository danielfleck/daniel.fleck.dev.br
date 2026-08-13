"""Gera e confere a documentação MkDocs em ``site/docs/``.

Fontes:
- Markdown: ``mkdocs/docs/``
- manual operacional canônico: ``SCRIPTS.md``
- cabeçalhos da documentação: ``mkdocs/.htaccess``

Saída pública:
- ``site/docs/``

O build sincroniza automaticamente ``SCRIPTS.md`` para a página
``mkdocs/docs/desenvolvimento/scripts-python.md`` e copia o .htaccess
específico da documentação após o ``mkdocs build --clean``.
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
SCRIPTS_SOURCE = PROJECT_ROOT / "SCRIPTS.md"
SCRIPTS_DOC = PROJECT_ROOT / "mkdocs" / "docs" / "desenvolvimento" / "scripts-python.md"
DOCS_HTACCESS_SOURCE = PROJECT_ROOT / "mkdocs" / ".htaccess"

GENERATED_NOTICE = """<!--
GENERATED FROM /SCRIPTS.md
NÃO EDITAR MANUALMENTE ESTA CÓPIA.
Execute: python scripts/build_docs.py
-->

"""

def scripts_doc_content() -> str:
    return GENERATED_NOTICE + SCRIPTS_SOURCE.read_text(encoding="utf-8")

def sync_scripts_doc(write: bool) -> bool:
    expected = scripts_doc_content()
    current = SCRIPTS_DOC.read_text(encoding="utf-8") if SCRIPTS_DOC.exists() else None
    if current == expected:
        return False
    if write:
        SCRIPTS_DOC.parent.mkdir(parents=True, exist_ok=True)
        SCRIPTS_DOC.write_text(expected, encoding="utf-8")
    return True

def snapshot(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result

def normalize_sitemap_gzip(root: Path) -> None:
    xml = root / "sitemap.xml"
    gz = root / "sitemap.xml.gz"
    if xml.exists():
        gz.write_bytes(gzip.compress(xml.read_bytes(), mtime=0))

def install_docs_htaccess(destination: Path) -> None:
    if not DOCS_HTACCESS_SOURCE.is_file():
        raise RuntimeError(f"Fonte do .htaccess não encontrada: {DOCS_HTACCESS_SOURCE}")
    shutil.copy2(DOCS_HTACCESS_SOURCE, destination / ".htaccess")

def run_mkdocs(destination: Path) -> None:
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
    process = subprocess.run(command, cwd=PROJECT_ROOT)
    if process.returncode != 0:
        raise RuntimeError("mkdocs build falhou.")

    normalize_sitemap_gzip(destination)
    install_docs_htaccess(destination)

def main() -> int:
    parser = argparse.ArgumentParser(description="Gera e confere a documentação MkDocs.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--hook", action="store_true")
    args = parser.parse_args()

    for required in (CONFIG, SCRIPTS_SOURCE, DOCS_HTACCESS_SOURCE):
        if not required.is_file():
            print(f"Arquivo obrigatório ausente: {required}")
            return 1

    if args.check:
        if sync_scripts_doc(write=False):
            print("Cópia MkDocs de SCRIPTS.md está desatualizada.")
            print("Execute: python scripts/build_docs.py")
            return 2

        with tempfile.TemporaryDirectory(prefix="mkdocs-check-") as temporary:
            temp_output = Path(temporary) / "site"
            try:
                run_mkdocs(temp_output)
            except RuntimeError as exc:
                print(exc)
                return 1

            if snapshot(temp_output) != snapshot(OUTPUT):
                print("Documentação gerada está desatualizada.")
                print("Execute: python scripts/build_docs.py")
                return 2

        print("MkDocs: site/docs e o espelho de SCRIPTS.md estão atualizados.")
        return 0

    before_output = snapshot(OUTPUT)
    scripts_changed = sync_scripts_doc(write=True)

    try:
        run_mkdocs(OUTPUT)
    except RuntimeError as exc:
        print(exc)
        return 1

    output_changed = before_output != snapshot(OUTPUT)

    if scripts_changed:
        print("MkDocs: espelho de SCRIPTS.md foi atualizado.")
    if output_changed:
        print("MkDocs: site/docs foi atualizado.")

    if args.hook and (scripts_changed or output_changed):
        print(
            "Commit interrompido: o build da documentação alterou arquivos. "
            "Revise, execute git add -A e repita o commit."
        )
        return 3

    if not scripts_changed and not output_changed:
        print("MkDocs: nenhum arquivo precisou ser alterado.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
