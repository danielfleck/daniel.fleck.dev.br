"""Remove resumos de Confluence que foram colocados indevidamente no MkDocs.

Execute uma vez e depois rode scripts/build_docs.py -- o build --clean remove
também as páginas HTML derivadas dessas fontes.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "mkdocs/docs/governanca/controle-versoes-legais-resumo.md",
    "mkdocs/docs/governanca/due-diligence-kinghost-resumo.md",
    "mkdocs/docs/governanca/enquadramento-pequeno-porte-resumo.md",
    "mkdocs/docs/governanca/fronteira-documental-resumo.md",
    "mkdocs/docs/governanca/legitimo-interesse-resumo.md",
    "mkdocs/docs/governanca/matriz-documentos-kinghost-resumo.md",
    "mkdocs/docs/governanca/matriz-normativa-resumo.md",
    "mkdocs/docs/governanca/registro-operacoes-tratamento-resumo.md",
    "mkdocs/docs/governanca/seguranca-incidentes-resumo.md",
    "mkdocs/docs/governanca/titulares-requisicoes-resumo.md",
]

def main() -> int:
    removed = 0
    for relative in FILES:
        path = ROOT / relative
        if path.exists():
            path.unlink()
            removed += 1
            print("Removido:", relative)
        else:
            print("Já ausente:", relative)

    print(f"Concluído: {removed} arquivo(s) removido(s).")
    print("Agora execute: python scripts/build_docs.py")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
