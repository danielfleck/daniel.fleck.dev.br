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

<!-- COMPLIANCE-MAINTENANCE:START -->

## 23. Gate de conformidade em todo commit

O pre-commit executa:

```bash
python scripts/compliance_gate.py --staged --enforce
```

O objetivo é **lembrar e bloquear inconsistências locais óbvias**, não declarar que a legislação continua vigente sem pesquisa.

O gate:
- informa a data da última revisão completa;
- avisa quando a revisão trimestral se aproxima;
- bloqueia quando a revisão está muito atrasada;
- detecta mudança em documentos legais sem racional/controle correspondente;
- lembra de revisar coleta, e-mail, terceiros, CSP, MkDocs e rede.

Depois de concluir uma revisão completa:

```bash
python scripts/ack_compliance_review.py
git add governance/compliance-status.json
```

Para registrar uma data específica:

```bash
python scripts/ack_compliance_review.py --date 2026-11-14
```

## 24. Validar racional dos documentos legais

```bash
python scripts/validate_legal_rationale.py
```

Exige:
- `AI-LEGAL-RATIONALE`;
- 16 marcadores da V7 do Aviso de Privacidade;
- 18 marcadores da V6 dos Termos;
- documentos de racional no MkDocs.

Comentários HTML são públicos. Não coloque neles evidência sensível.

## 25. Validar superfície pública de contato

```bash
python scripts/validate_contact_surface.py
```

Confere:
- existência de `/contato/`;
- ausência do endereço de e-mail pessoal antigo;
- ausência do endereço oficial em texto literal no HTML público/template;
- presença do mecanismo `PRIVACY-LINK-GUARD`.

O objetivo é reduzir coleta automática simples. Isso não torna o endereço secreto.

## 26. Conferir DNS do e-mail

Requer `dig`:

```bash
python scripts/check_email_dns.py
```

O estado documentado desta release é:

```text
SPF:   v=spf1 include:_spf.kinghost.net -all
DMARC: v=DMARC1; p=none;
```

O script não altera DNS.

## 27. Conferir autenticação de uma mensagem entregue

Salve localmente uma mensagem de teste como `.eml` e **não faça commit** do arquivo:

```bash
python scripts/check_email_auth.py caminho/privado/teste.eml
```

O script resume:
- `Authentication-Results`;
- SPF;
- DKIM;
- DMARC;
- domínios `d=` encontrados.

Ele não faz validação criptográfica independente; usa os resultados adicionados pelo servidor recebedor.

## 28. Relatórios agregados DMARC

Se futuramente for configurado:

```text
rua=mailto:dmarc-reports@fleck.dev.br
```

guarde os relatórios em diretório privado/ignorado e use:

```bash
python scripts/parse_dmarc_report.py dmarc-reports/relatorio.xml
python scripts/parse_dmarc_report.py dmarc-reports/relatorio.xml.gz
```

Não habilite `ruf` apenas para “ter mais dados”. Relatórios de falha podem aumentar exposição de dados e volume operacional.

## 29. Superfícies administrativas da KingHost

Após deploy ou revisão mensal:

```bash
python scripts/check_admin_surfaces.py \
  --base-url https://daniel.fleck.dev.br
```

O script verifica anonimamente:

```text
/stats/
/varnish-stats/
```

Ele não tenta senha nem faz força bruta.

Na hospedagem KingHost atualmente utilizada, `/stats/` pode redirecionar para
o AWStats e responder HTTP 200 anonimamente. Esse comportamento é tratado
como **WARN conhecido da infraestrutura do provedor** e não reprova sozinho
a validação. `/varnish-stats/` continua sendo verificado normalmente.


## 30. Validação de produção sem depender de cache do crawler

```bash
python scripts/validate_production_nocache.py \
  --base-url https://daniel.fleck.dev.br
```

O script usa:
- query string única;
- `Cache-Control: no-cache, no-store`;
- `Pragma: no-cache`.

Depois execute também a auditoria Chromium:

```bash
python scripts/audit_network.py \
  --base-url https://daniel.fleck.dev.br \
  --all \
  --report dist/network-audit-production.json
```

## 31. Fluxo completo de uma release jurídica

Antes do commit:

```bash
python -m unittest discover -s tests -v
python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/validate_docs.py
python scripts/validate_contact_surface.py
python scripts/validate_legal_rationale.py
python scripts/check_email_dns.py
python scripts/audit_network.py --all
python scripts/serve.py
```

Revise visualmente:
- home;
- currículo;
- `/contato/`;
- Aviso de Privacidade;
- Termos;
- `/docs/`;
- modal de link externo;
- modal de e-mail;
- navegação por teclado;
- tela pequena.

Depois:

```bash
git status
git diff
git add -A
git diff --cached
git commit -m "feat: consolida privacidade e segurança do contato"
git push
```

Após deploy:

```bash
python scripts/validate_production_nocache.py \
  --base-url https://daniel.fleck.dev.br

python scripts/validate.py \
  --production-url https://daniel.fleck.dev.br \
  --network

python scripts/validate_docs.py \
  --production-url https://daniel.fleck.dev.br/docs/

python scripts/check_admin_surfaces.py \
  --base-url https://daniel.fleck.dev.br
```

Preencha uma cópia **privada** do modelo de evidência pós-deploy.

## 32. Revisão trimestral

A fonte de estado é:

```text
governance/compliance-status.json
```

A revisão completa deve conferir:
- normas oficiais vigentes;
- contratos/políticas KingHost;
- cadeia do serviço de e-mail;
- transferências internacionais;
- SPF/DKIM/DMARC;
- antispam;
- retenção;
- `/stats`;
- terceiros automáticos;
- CSP/headers;
- auditoria de rede;
- Aviso de Privacidade;
- Termos;
- MkDocs/Confluence.

O arquivo `calendar/revisoes-conformidade.ics` do pacote pode ser importado no calendário.

<!-- COMPLIANCE-MAINTENANCE:END -->

## Validação de HTTPS, HSTS e security.txt

**Motivo:** detectar regressão no redirecionamento HTTP→HTTPS, ausência/encurtamento de HSTS e expiração ou remoção do canal padronizado de segurança.

**Fundamento técnico:** RFC 6797, RFC 9116, configuração Apache/KingHost e política pública `/seguranca/`.

Validação local:

```bash
python scripts/validate_transport_security.py
```

A validação local confere:
- existência de `site/.htaccess`;
- regra HTTPS;
- HSTS com `max-age` final mínimo de 31536000;
- `security.txt`;
- `Contact`, `Expires` e `Canonical`;
- página `/seguranca/`;
- inclusão da página no rebuild/sitemap.

Produção:

```bash
python scripts/validate_transport_security.py \
  --production-url https://daniel.fleck.dev.br
```

A validação de produção:
- acessa HTTP sem seguir o redirect;
- exige `301` ou `308`;
- confirma preservação de caminho e query;
- verifica HSTS na resposta HTTPS;
- verifica `security.txt`;
- verifica `Content-Type: text/plain`;
- verifica `/seguranca/`.

### Fase de implantação

Durante a fase curta com `302` e `max-age=300`, execute:

```bash
python scripts/validate_transport_security.py --allow-test-stage
```

O script aceita esse estado somente como etapa temporária.

Depois dos testes, aplique o `.htaccess` final e execute sem a opção:

```bash
python scripts/validate_transport_security.py
```

### Pre-commit

Depois que a configuração definitiva estiver publicada e estável:

```sh
"$PY" scripts/validate_transport_security.py || exit 1
```

Não coloque `--production-url` no pre-commit.
