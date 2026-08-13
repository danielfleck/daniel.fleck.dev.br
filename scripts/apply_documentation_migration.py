"""Aplica ajustes pontuais da migração documental Jira × Confluence × MkDocs.

O script foi preparado para ser executado uma única vez no repositório atual.
Ele evita substituir páginas inteiras e altera apenas os trechos explicitamente
mapeados nesta migração. Revise sempre ``git diff`` antes do commit.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def update(path: Path, transform) -> bool:
    if not path.exists():
        print("AVISO: arquivo não encontrado:", path.relative_to(ROOT))
        return False
    old = path.read_text(encoding="utf-8")
    new = transform(old)
    if new == old:
        return False
    path.write_text(new, encoding="utf-8")
    print("ALTERADO:", path.relative_to(ROOT))
    return True


def insert_after_marker(text: str, marker: str, html: str, fingerprint: str) -> str:
    if fingerprint in text:
        return text
    if marker not in text:
        raise RuntimeError(f"Marcador não encontrado: {marker}")
    return text.replace(marker, marker + "\n" + html, 1)


def patch_terms(text: str) -> str:
    # Correção apenas estrutural de navegação. Não altera o conteúdo jurídico.
    text = text.replace(
        'href="#privacidade" onclick="showSection(\'privacidade\'); return false;"',
        'href="/privacidade/"',
    )
    text = text.replace(
        'href="#privacidade" onclick="showSection(&#39;privacidade&#39;); return false;"',
        'href="/privacidade/"',
    )
    return text


def patch_confluence_blog(text: str) -> str:
    note = (
        '<aside class="article-note"><strong>Atualização:</strong> o modelo documental evoluiu '
        'posteriormente. O Jira passou a concentrar o trabalho e sua execução; o Confluence, '
        'o contexto, as decisões, a estratégia e as retrospectivas; e o MkDocs, integrado ao '
        'repositório do site, passou a documentar o produto técnico e sua implementação.</aside>'
    )
    return insert_after_marker(text, '<!-- CONTENT-BODY:START -->', note, "o modelo documental evoluiu posteriormente")


def patch_roadmap_blog(text: str) -> str:
    note = (
        '<aside class="article-note"><strong>Atualização de governança:</strong> este artigo registra '
        'uma etapa histórica. O repositório Roadmap GitHub não é mais a fonte oficial do trabalho. '
        'O trabalho e seu estado passaram ao Jira; o Confluence passou a manter resumo/contexto; e o '
        'MkDocs passou a preservar a documentação completa e versionada.</aside>'
    )
    return insert_after_marker(text, '<!-- CONTENT-BODY:START -->', note, "este artigo registra uma etapa histórica")


def patch_home(text: str) -> str:
    return text.replace("Ver plano de atualização", "Ver histórico do plano 2026")


def patch_roadmap_page(text: str) -> str:
    text = text.replace(
        "Plano de atualização técnica — 2026 | Daniel Fleck",
        "Histórico do plano de atualização técnica — 2026 | Daniel Fleck",
    )
    text = text.replace(
        'content="Plano de atualização profissional e técnica em 2026."',
        'content="Registro histórico do plano de atualização técnica utilizado em 2026; o trabalho corrente é gerenciado no Jira."',
    )
    replacement = '''<main class="container"><section class="section">
<header class="page-header"><div class="section-kicker">Registro histórico</div><h1>Histórico do plano de atualização técnica — 2026</h1><p class="page-summary">Esta página preserva o plano público utilizado em uma etapa anterior da transição profissional. Ela não representa o backlog nem o estado corrente do trabalho.</p></header>
<div class="legal-summary"><strong>Modelo atual:</strong> o trabalho e seu andamento são registrados no Jira; contexto, estratégia, decisões e retrospectivas ficam no Confluence; a documentação do produto <code>daniel.fleck.dev.br</code> e de sua implementação técnica fica no MkDocs.</div>
<article class="card"><h2>Por que esta página foi preservada?</h2><p>O plano de 2026 faz parte do histórico do projeto e ajuda a compreender a evolução do processo de atualização técnica. Preservá-lo como registro histórico evita reescrever retrospectivamente o caminho percorrido, mas impede que uma página estática antiga concorra com o Jira como fonte de verdade do trabalho atual.</p></article>
<article class="card"><h2>Como interpretar as referências antigas</h2><p>Artigos e páginas antigas podem mencionar o Roadmap GitHub ou o Confluence como locais centrais de acompanhamento. Essas referências descrevem o modelo utilizado naquele momento. A arquitetura documental foi posteriormente refinada para separar trabalho, decisão e estado técnico resultante.</p></article>
<article class="card"><h2>Fontes atuais</h2><ul><li><strong>Jira:</strong> tarefas, épicos, prioridades, bloqueios e andamento.</li><li><strong>Confluence:</strong> resumo, contexto e links para documentos duráveis.</li><li><strong>MkDocs:</strong> documentação completa do produto, implementação e governança que precisa de preservação.</li><li><strong>GitHub:</strong> código, commits, histórico e documentação técnica versionada.</li></ul></article>
</section></main>'''
    pattern = re.compile(r'<main class="container"><section class="section">.*?</section></main>', re.S)
    if not pattern.search(text):
        raise RuntimeError("Não foi possível localizar o bloco principal de site/roadmap/index.html")
    return pattern.sub(replacement, text, count=1)


def remove_ineffective_frame_ancestors(text: str) -> str:
    # frame-ancestors não tem efeito em CSP entregue por <meta>. A proteção
    # definitiva deve ser configurada/testada como header HTTP no servidor.
    return text.replace("frame-ancestors 'none'; ", "").replace("frame-ancestors 'none';", "")


def scan_legacy() -> list[str]:
    findings: list[str] = []
    patterns = ["showSection(", 'href="#privacidade"', " onclick="]
    for root in (SITE, ROOT / "templates"):
        if not root.exists():
            continue
        for path in root.rglob("*.html"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in patterns:
                if pattern in text:
                    findings.append(f"{path.relative_to(ROOT)}: {pattern}")
    return findings


def clean_generated() -> None:
    candidates = [
        ROOT / "daniel_fleck_site.egg-info",
        ROOT / "dist",
        ROOT / "mkdocs/site",
    ]
    for path in candidates:
        if path.is_dir():
            shutil.rmtree(path)
            print("REMOVIDO:", path.relative_to(ROOT))
        elif path.exists():
            path.unlink()
            print("REMOVIDO:", path.relative_to(ROOT))


def remove_legacy_docs() -> None:
    candidates = [
        ROOT / "SCRIPTS.md",
        ROOT / "docs/STRUCTURE.md",
        ROOT / "docs/AI-MAINTENANCE.md",
        ROOT / "docs/VALIDATION.md",
    ]
    for path in candidates:
        if path.exists():
            path.unlink()
            print("REMOVIDO:", path.relative_to(ROOT))
    docs = ROOT / "docs"
    if docs.is_dir() and not any(docs.iterdir()):
        docs.rmdir()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean-generated", action="store_true")
    parser.add_argument("--remove-legacy-docs", action="store_true")
    args = parser.parse_args()

    update(SITE / "termos/index.html", patch_terms)
    update(SITE / "blog/confluence-diario-tecnico-transicao/index.html", patch_confluence_blog)
    update(SITE / "blog/roadmap-transicao-ti-github/index.html", patch_roadmap_blog)
    update(SITE / "index.html", patch_home)
    update(SITE / "roadmap/index.html", patch_roadmap_page)

    # Retira a diretiva sem efeito dos CSPs em meta e do gerador de páginas.
    for root in (SITE, ROOT / "templates"):
        if root.exists():
            for path in root.rglob("*.html"):
                update(path, remove_ineffective_frame_ancestors)
    update(ROOT / "scripts/rebuild.py", remove_ineffective_frame_ancestors)

    if args.clean_generated:
        clean_generated()
    if args.remove_legacy_docs:
        remove_legacy_docs()

    findings = scan_legacy()
    if findings:
        print("\nREVISÃO MANUAL — vestígios encontrados:")
        for item in findings:
            print(" -", item)
    else:
        print("\nNenhum vestígio showSection/#privacidade/onclick foi encontrado nos HTMLs verificados.")

    print("\nIMPORTANTE:")
    print("- A correção do link dos Termos é estrutural e não altera o texto jurídico; Termos permanecem V3.")
    print("- A Política de Privacidade permanece V4.")
    print("- frame-ancestors foi removido do CSP em meta por ser ineficaz nesse modo; configure a proteção definitiva como header HTTP somente após teste no site e em /docs/.")
    print("- Execute rebuild, build_docs, validate, testes e git diff antes do commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
