# Guia dos scripts de manutenção do site

Este arquivo permanece na **raiz do repositório** e é o manual operacional canônico dos scripts Python. A página correspondente no MkDocs é gerada automaticamente por `scripts/build_docs.py`; não mantenha duas cópias manuais.

## 1. Preparação do ambiente

Requisito: **Python 3.10 ou superior**.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[audit]"
python -m playwright install chromium
python scripts/install_hooks.py
```

O grupo opcional `audit` instala Playwright, utilizado somente para a auditoria dinâmica de rede.

## 2. Rotina para criar um novo post

```bash
source .venv/bin/activate
python scripts/create_content.py blog
```

O script cria `site/blog/<slug>/index.html` e executa `rebuild.py` automaticamente. Depois edite somente o trecho entre:

```html
<!-- CONTENT-BODY:START -->
...
<!-- CONTENT-BODY:END -->
```

Em seguida:

```bash
python scripts/rebuild.py
python scripts/validate.py
python scripts/audit_network.py --all
python scripts/serve.py

git status
git diff
git add -A
git commit -m "Adiciona post ..."
git push
```

`serve.py` é opcional, mas recomendado para revisão visual.

## 3. Alterar um post existente

Edite `site/blog/<slug>/index.html` e execute:

```bash
python scripts/rebuild.py
python scripts/validate.py
python scripts/audit_network.py --all
python scripts/serve.py
```

Depois revise o `git diff`, faça commit e push.

## 4. Criar item de Portfólio

```bash
python scripts/create_content.py portfolio
```

Depois de editar o corpo:

```bash
python scripts/rebuild.py
python scripts/validate.py
python scripts/audit_network.py --all
python scripts/serve.py
```

## 5. Criar registro em Erros e Soluções

```bash
python scripts/create_content.py erro
```

Depois:

```bash
python scripts/rebuild.py
python scripts/validate.py
python scripts/audit_network.py --all
python scripts/serve.py
```

## 6. Alterar documentação MkDocs

Edite somente arquivos em:

```text
mkdocs/docs/
```

Para a página de scripts, edite **somente `SCRIPTS.md` na raiz**.

Depois:

```bash
python scripts/build_docs.py
python scripts/validate.py
python scripts/audit_network.py --all
python scripts/serve.py
```

`build_docs.py` também:
- sincroniza `SCRIPTS.md` para `mkdocs/docs/desenvolvimento/scripts-python.md`;
- executa `mkdocs build --clean --strict`;
- copia `mkdocs/.htaccess` para `site/docs/.htaccess`;
- normaliza `sitemap.xml.gz`.

## 7. Atualizar Política de Privacidade ou Termos

Alterações textuais nos documentos jurídicos exigem nova versão sequencial.

Rotina:

```bash
# editar site/privacidade/index.html e/ou site/termos/index.html

python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/audit_network.py --all
python scripts/serve.py
```

Antes de publicar, confira se a data/hora indicada no documento corresponde ao momento real de publicação.

Após o deploy:

```bash
python scripts/validate.py \
  --production-url https://daniel.fleck.dev.br \
  --network
```

Guarde a evidência dos headers e da auditoria no arquivo restrito de validação pós-deploy.

## 8. `scripts/create_content.py`

Cria conteúdo novo a partir de templates:

```bash
python scripts/create_content.py blog
python scripts/create_content.py portfolio
python scripts/create_content.py erro
```

O corpo editorial é editado depois no bloco `CONTENT-BODY`.

## 9. `scripts/rebuild.py`

Reconstrói índices, tags, sitemap, SEO, JSON-LD, navegação e rodapé.

```bash
python scripts/rebuild.py
python scripts/rebuild.py --check
python scripts/rebuild.py --hook
```

Depois de aplicar a migração de segurança, o script não deve voltar a gerar `frame-ancestors` dentro de CSP entregue por `<meta>`.

## 10. `scripts/build_docs.py`

```bash
python scripts/build_docs.py
python scripts/build_docs.py --check
python scripts/build_docs.py --hook
```

Fontes:
- `mkdocs/docs/`
- `SCRIPTS.md`
- `mkdocs/.htaccess`

Saída:
- `site/docs/`

## 11. `scripts/validate.py`

Validação estática:

```bash
python scripts/validate.py
```

Também confere:
- documentos legais V5/V4;
- ausência de `frame-ancestors` em CSP por `<meta>`;
- ausência de `repo_url` e analytics no MkDocs;
- sincronização de `SCRIPTS.md`;
- `.htaccess` da raiz e da documentação;
- build MkDocs atualizado;
- links, SEO, JSON-LD, sitemap e recursos locais.

Com auditoria dinâmica:

```bash
python scripts/validate.py --network
```

Produção:

```bash
python scripts/validate.py \
  --production-url https://daniel.fleck.dev.br \
  --network
```

## 12. `scripts/audit_network.py`

Abre o site em Chromium headless e observa requisições reais de rede.

Auditoria rápida:

```bash
python scripts/audit_network.py
```

Todas as páginas:

```bash
python scripts/audit_network.py --all
```

Produção:

```bash
python scripts/audit_network.py \
  --base-url https://daniel.fleck.dev.br \
  --all \
  --report dist/network-audit-production.json
```

Por padrão, hosts externos não autorizados causam falha. A tentativa é registrada e abortada antes de ser concluída.

## 13. `scripts/apply_security_migration.py`

Executar **uma vez** durante esta migração:

```bash
python scripts/apply_security_migration.py
```

Ele remove `frame-ancestors 'none'` de CSPs entregues por `<meta>` em HTML/templates e ajusta `rebuild.py` para não reintroduzir a diretiva. A proteção passa a ser entregue por cabeçalho HTTP nos arquivos `.htaccess`.

## 14. `scripts/serve.py`

```bash
python scripts/serve.py
```

Serve apenas `site/` em `http://127.0.0.1:8000/`.

## 15. `scripts/install_hooks.py`

```bash
python scripts/install_hooks.py
```

Ativa `.githooks/pre-commit` e `.githooks/pre-push`.

## 16. Pre-commit

No `git commit`:

```text
rebuild.py --hook
  ↓
build_docs.py --hook
  ↓
validate.py
```

Se um gerador alterar arquivos, o commit é interrompido para revisão e novo `git add -A`.

## 17. Pre-push

No `git push`:

```text
audit_network.py --all
```

O push é bloqueado se o navegador tentar acessar host externo não autorizado.

## 18. Testes automatizados

```bash
python -m unittest discover -s tests -v
```

Recomendado depois de alterações nos scripts Python.

## 19. Rotina após alteração de script

```bash
python -m unittest discover -s tests -v
python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/audit_network.py --all
python scripts/serve.py
```

## 20. Validação pós-deploy dos headers da KingHost

Use:

```bash
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/docs/
```

Na raiz, confirme no mínimo:
- `Content-Security-Policy` com `frame-ancestors 'none'`;
- `X-Frame-Options: DENY`;
- `Referrer-Policy: no-referrer`;
- `X-Content-Type-Options: nosniff`.

Em `/docs/`, confirme também:
- `connect-src 'self'`;
- `script-src 'self' 'unsafe-inline'`.

Se a KingHost estiver usando cache intermediário, limpe o cache antes do teste.

## 21. Ordem resumida de publicação

```text
editar
  ↓
rebuild
  ↓
build_docs
  ↓
validate
  ↓
audit_network
  ↓
serve/revisão
  ↓
commit
  ↓
push
  ↓
deploy
  ↓
validate --production-url ... --network
  ↓
guardar evidências restritas
```
