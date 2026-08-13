# Guia dos scripts de manutenção do site

Este arquivo permanece na **raiz do repositório** e é o manual operacional canônico dos scripts Python. A página equivalente no MkDocs é gerada automaticamente por `scripts/build_docs.py`.

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

No Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[audit]"
python -m playwright install chromium
python scripts/install_hooks.py
```

Depois de atualizar a versão do Playwright, execute novamente `python -m playwright install chromium` se o navegador gerenciado deixar de ser encontrado.

## 2. Sequência completa antes de um commit importante

Para mudanças em scripts, MkDocs, segurança, Política de Privacidade, Termos ou estrutura:

```bash
source .venv/bin/activate

python -m unittest discover -s tests -v
python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/validate_docs.py
python scripts/audit_network.py --all
python scripts/serve.py
```

Depois da revisão visual:

```bash
git status
git diff
git add -A
git status
git diff --cached
git commit -m "Descrição da alteração"
git push
```

O `serve.py` é opcional para alterações sem efeito visual, mas é recomendado antes de publicação relevante.

## 3. Criar um novo post

```bash
python scripts/create_content.py blog
```

O script cria `site/blog/<slug>/index.html` e executa `rebuild.py` automaticamente. Edite somente:

```html
<!-- CONTENT-BODY:START -->
...
<!-- CONTENT-BODY:END -->
```

Depois:

```bash
python scripts/rebuild.py
python scripts/build_docs.py --check
python scripts/validate.py
python scripts/validate_docs.py
python scripts/audit_network.py --all
python scripts/serve.py
```

## 4. Alterar um post existente

Edite `site/blog/<slug>/index.html` e execute a mesma sequência de validação do item anterior.

## 5. Criar item de Portfólio

```bash
python scripts/create_content.py portfolio
```

Depois de editar o corpo:

```bash
python scripts/rebuild.py
python scripts/validate.py
python scripts/validate_docs.py
python scripts/audit_network.py --all
python scripts/serve.py
```

## 6. Criar registro em Erros e Soluções

```bash
python scripts/create_content.py erro
```

Não marque hipótese como causa confirmada e não marque como resolvido sem validação.

Depois:

```bash
python scripts/rebuild.py
python scripts/validate.py
python scripts/validate_docs.py
python scripts/audit_network.py --all
python scripts/serve.py
```

## 7. Alterar documentação MkDocs

Edite os arquivos-fonte em `mkdocs/docs/`.

**Exceção:** para a documentação dos scripts, edite somente `SCRIPTS.md` na raiz.

Depois:

```bash
python scripts/build_docs.py
python scripts/validate.py
python scripts/validate_docs.py
python scripts/audit_network.py --all
python scripts/serve.py
```

`build_docs.py`:
- sincroniza `SCRIPTS.md` para `mkdocs/docs/desenvolvimento/scripts-python.md`;
- executa `mkdocs build --clean --strict`;
- copia `mkdocs/.htaccess` para `site/docs/.htaccess`;
- normaliza `sitemap.xml.gz`.

## 8. Atualizar Política de Privacidade ou Termos

Alteração textual exige nova versão sequencial apenas do documento alterado.

Depois da edição:

```bash
python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/validate_docs.py
python scripts/audit_network.py --all
python scripts/serve.py
```

Após o deploy:

```bash
python scripts/validate.py \
  --production-url https://daniel.fleck.dev.br \
  --network

python scripts/validate_docs.py \
  --production-url https://daniel.fleck.dev.br/docs/
```

Registre as evidências pós-deploy em armazenamento restrito.

## 9. `scripts/create_content.py`

```bash
python scripts/create_content.py blog
python scripts/create_content.py portfolio
python scripts/create_content.py erro
```

Cria conteúdo a partir dos templates e executa o rebuild inicial.

## 10. `scripts/rebuild.py`

```bash
python scripts/rebuild.py
python scripts/rebuild.py --check
python scripts/rebuild.py --hook
```

Reconstrói navegação, rodapé, SEO, JSON-LD, índices, tags, sitemap e demais artefatos derivados do site principal.

## 11. `scripts/build_docs.py`

```bash
python scripts/build_docs.py
python scripts/build_docs.py --check
python scripts/build_docs.py --hook
```

Fonte: `mkdocs/docs/`, `SCRIPTS.md` e `mkdocs/.htaccess`.  
Saída: `site/docs/`.

## 12. `scripts/validate.py`

```bash
python scripts/validate.py
```

Valida o site principal, documentos legais, coerência documental, configuração do MkDocs, hooks, `.htaccess`, sitemap, links, SEO e estado dos builds.

Para conferir headers da produção e executar a auditoria dinâmica:

```bash
python scripts/validate.py \
  --production-url https://daniel.fleck.dev.br \
  --network
```

## 13. `scripts/validate_docs.py`

```bash
python scripts/validate_docs.py
```

Faz a validação específica da saída Material for MkDocs, incluindo referências locais, CSS, carregamentos externos e presença da política de segurança da documentação.

Produção:

```bash
python scripts/validate_docs.py \
  --production-url https://daniel.fleck.dev.br/docs/
```

## 14. `scripts/audit_network.py`

Auditoria rápida:

```bash
python scripts/audit_network.py
```

Todas as páginas locais:

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

O script abre Chromium headless, observa HTTP/HTTPS/WS/WSS e aborta uma tentativa para host não autorizado antes de concluí-la.

## 15. `scripts/serve.py`

```bash
python scripts/serve.py
```

Serve somente `site/` em `http://127.0.0.1:8000/`.

## 16. `scripts/install_hooks.py`

```bash
python scripts/install_hooks.py
```

Ativa os hooks versionados em `.githooks/`. Execute depois de cada clone.

## 17. `.githooks/pre-commit`

O `git commit` executa:

```text
rebuild.py --hook
   ↓
build_docs.py --hook
   ↓
validate.py
   ↓
validate_docs.py
```

Se um gerador alterar arquivos, o commit é interrompido para revisão e novo `git add -A`.

## 18. `.githooks/pre-push`

O `git push` executa:

```text
audit_network.py --all
```

O push é bloqueado quando a auditoria falha ou identifica host externo não autorizado.

## 19. Migrações de uso único

`scripts/apply_security_migration.py` e `scripts/apply_documentation_migration.py` são scripts de migração histórica. **Não fazem parte da rotina diária** e não devem ser reexecutados sem revisar previamente seu objetivo e o estado atual do repositório.

## 20. Testes automatizados

```bash
python -m unittest discover -s tests -v
```

Especialmente recomendados depois de mudanças nos scripts Python.

## 21. Headers após deploy

```bash
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/docs/
```

Na raiz, confirme:
- `Content-Security-Policy` com `frame-ancestors 'none'`;
- `X-Frame-Options: DENY`;
- `Referrer-Policy: no-referrer`;
- `X-Content-Type-Options: nosniff`.

Em `/docs/`, confirme também:
- `connect-src 'self'`;
- `script-src 'self' 'unsafe-inline'`.

## 22. Ordem resumida

```text
editar
  ↓
testes
  ↓
rebuild
  ↓
build_docs
  ↓
validate
  ↓
validate_docs
  ↓
audit_network
  ↓
serve/revisão
  ↓
git diff
  ↓
commit
  ↓
pre-commit
  ↓
push
  ↓
pre-push
  ↓
deploy
  ↓
validação de produção
  ↓
evidência restrita
```
