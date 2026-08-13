# daniel.fleck.dev.br — site estático multipágina

O conteúdo publicado permanece **HTML + CSS + JavaScript estático**. Python, MkDocs e Playwright são ferramentas locais de criação, build, validação e auditoria.

## Estrutura principal

- `site/`: raiz pública.
- `site/docs/`: build público do MkDocs.
- `mkdocs/docs/`: Markdown-fonte da documentação.
- `scripts/`: automações locais.
- `templates/`: templates e parciais do site principal.
- `SCRIPTS.md`: manual operacional canônico.
- `site/.htaccess`: cabeçalhos comuns.
- `mkdocs/.htaccess`: fonte do cabeçalho específico da documentação.
- `site/docs/.htaccess`: cópia gerada por `build_docs.py`.

## Ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[audit]"
python -m playwright install chromium
python scripts/install_hooks.py
```

## Fluxo de validação

```bash
python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/audit_network.py --all
python scripts/serve.py
```

## Privacidade por arquitetura

A configuração atual:
- não usa analytics próprio, pixels ou publicidade;
- mantém fontes do MkDocs locais (`font: false`);
- não usa `repo_url` do Material for MkDocs;
- apresenta GitHub apenas como link normal;
- restringe `connect-src` de `/docs/` a `'self'`;
- usa auditoria headless para detectar conexões externas em runtime;
- documenta o uso funcional de Web Storage do Material for MkDocs na Política de Privacidade.

## Documentação dos scripts

Consulte [`SCRIPTS.md`](SCRIPTS.md).
