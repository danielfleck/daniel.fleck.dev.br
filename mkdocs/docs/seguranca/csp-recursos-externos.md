# CSP e recursos externos

## Estado atual

O site principal mantém CSP restritiva em `<meta>` para as diretivas compatíveis e recebe `frame-ancestors 'none'` por cabeçalho HTTP.

`/docs/` recebe uma CSP própria por `site/docs/.htaccess`, incluindo:

```text
connect-src 'self'
frame-ancestors 'none'
```

O Material for MkDocs usa JavaScript inline, motivo pelo qual a política de `/docs/` permite `'unsafe-inline'` em `script-src` enquanto essa implementação for necessária.

## Recursos externos

A configuração atual não utiliza `repo_url`, fontes Google, analytics nem CDN externa automática. O GitHub aparece apenas como link normal.

Links `<a>` externos não equivalem a carregar scripts, fontes, imagens ou iframes de terceiros.

## Barreira dinâmica

`scripts/audit_network.py` complementa a inspeção do HTML e falha se o navegador tentar comunicação para host externo não autorizado.

## Novos terceiros

Antes de adicionar integração externa automática:

1. identificar finalidade e fornecedor;
2. confirmar necessidade;
3. avaliar privacidade e segurança;
4. ajustar CSP pelo mínimo necessário;
5. revisar Política/Termos quando houver efeito material;
6. testar estaticamente e em navegador headless;
7. validar produção após o deploy.
