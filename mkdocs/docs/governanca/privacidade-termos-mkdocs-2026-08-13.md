# Privacidade e Termos após a inclusão do MkDocs

**Decisão registrada em:** 13/08/2026 às 18:11 (BRT, UTC-3)

## Mudanças materiais

A inclusão de `/docs/` trouxe três pontos que precisavam ser incorporados à governança:

1. Material for MkDocs contém suporte a `localStorage`/`sessionStorage`;
2. `repo_url` pode provocar consulta automática a dados públicos do GitHub;
3. a CSP do site principal não podia simplesmente ser copiada para `/docs/`, pois o Material usa JavaScript inline de inicialização.

## Decisões

- Política de Privacidade passa de V4 para **V5**.
- Termos de Uso passam de V3 para **V4**.
- `repo_url`/`repo_name` são removidos do MkDocs.
- GitHub permanece como link comum.
- `/docs/` recebe CSP própria com `connect-src 'self'`.
- `frame-ancestors 'none'` passa a ser entregue por cabeçalho HTTP.
- a raiz e `/docs/` recebem `Referrer-Policy: no-referrer`, `X-Frame-Options: DENY` e `X-Content-Type-Options: nosniff`.
- auditoria headless passa a complementar a validação estática.
- `SCRIPTS.md` permanece canônico na raiz e é espelhado automaticamente no MkDocs.
- evidência integral do atendimento KingHost permanece em armazenamento restrito; o MkDocs publica apenas a conclusão técnica necessária.

## Critério de fechamento

A mudança só deve ser considerada concluída quando:

```bash
python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/audit_network.py --all
```

passarem, e após o deploy:

```bash
python scripts/validate.py   --production-url https://daniel.fleck.dev.br   --network
```

também passar.
