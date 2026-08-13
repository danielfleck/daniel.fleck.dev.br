# Privacidade e Termos após a inclusão do MkDocs

**Decisão registrada em:** 13/08/2026 às 18:11 (BRT, UTC-3)  
**Estado:** implementação versionada no Git; fechamento operacional depende de deploy e validação de produção.

## Mudanças materiais

A inclusão de `/docs/` introduziu:
1. suporte do Material for MkDocs a `localStorage`/`sessionStorage`;
2. risco de consulta automática ao GitHub quando `repo_url` é usado;
3. JavaScript inline que exige política CSP própria para a documentação.

## Decisões

- Política de Privacidade: **V5**.
- Termos de Uso: **V4**.
- `repo_url`/`repo_name`: removidos.
- GitHub: link comum.
- fontes remotas: desabilitadas por `font: false`.
- `/docs/`: CSP própria com `connect-src 'self'`.
- anti-framing: `frame-ancestors 'none'` por header HTTP.
- raiz e `/docs/`: `Referrer-Policy: no-referrer`, `X-Frame-Options: DENY` e `X-Content-Type-Options: nosniff`.
- auditoria headless: complemento obrigatório da validação estática.
- `SCRIPTS.md`: canônico na raiz e espelhado automaticamente.
- atendimento integral KingHost: evidência restrita; MkDocs publica apenas as conclusões necessárias.
- resumos de governança: pertencem ao Confluence, não ao MkDocs.

## Critério de fechamento local

```bash
python -m unittest discover -s tests -v
python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/validate_docs.py
python scripts/audit_network.py --all
```

## Critério de fechamento em produção

```bash
python scripts/validate.py \
  --production-url https://daniel.fleck.dev.br \
  --network

python scripts/validate_docs.py \
  --production-url https://daniel.fleck.dev.br/docs/
```

A existência de um commit no GitHub não substitui a comprovação de que o webhook/deploy publicou esse commit.
