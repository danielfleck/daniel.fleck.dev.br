# CSP e cabeçalhos HTTP

## Objetivo

A proteção do site é dividida em dois níveis:

1. o site principal mantém uma CSP restritiva em `<meta>` para os recursos da página;
2. `frame-ancestors 'none'`, que não produz o efeito pretendido quando entregue apenas por `<meta>`, é enviado por cabeçalho HTTP.

A especificação CSP atual não admite `frame-ancestors` em política entregue por `<meta>`. Por isso a diretiva foi removida dos HTMLs/templates e transferida para `site/.htaccess`.

## Cabeçalhos da raiz

Arquivo canônico: `site/.htaccess`.

```apache
# Cabeçalhos comuns do site estático.
# Confirmar após o deploy com:
# curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/
#
# A CSP completa de recursos do site principal permanece também em <meta>.
# frame-ancestors precisa ser entregue como cabeçalho HTTP.

Header always set Content-Security-Policy "frame-ancestors 'none'"
Header always set X-Frame-Options "DENY"
Header always set Referrer-Policy "no-referrer"
Header always set X-Content-Type-Options "nosniff"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
```

## Política de `/docs/`

Arquivo-fonte: `mkdocs/.htaccess`.

O `build_docs.py` copia esse arquivo para `site/docs/.htaccess` depois do `mkdocs build --clean`.

```apache
# Política específica do Material for MkDocs.
# O tema possui JavaScript inline de inicialização; por isso script-src
# precisa permitir 'unsafe-inline' nesta área enquanto esse template for usado.
#
# connect-src 'self' impede fetch/XHR/WebSocket para hosts externos.
# Links <a> externos continuam permitidos quando o visitante decide clicar.

Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; worker-src 'self' blob:; media-src 'self'; manifest-src 'self'; frame-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests"
Header always set X-Frame-Options "DENY"
Header always set Referrer-Policy "no-referrer"
Header always set X-Content-Type-Options "nosniff"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
```

A exceção `script-src 'unsafe-inline'` existe porque Material for MkDocs utiliza JavaScript inline de inicialização. A exceção é limitada à documentação; o site principal não precisa dela para scripts.

`connect-src 'self'` é particularmente importante: impede conexões programáticas de `fetch`, XHR, WebSocket e APIs equivalentes para hosts externos.

## Validação

Após o deploy:

```bash
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/docs/
```

Também:

```bash
python scripts/validate.py --production-url https://daniel.fleck.dev.br --network
```

A validação em produção é obrigatória porque a KingHost informou que sua documentação não detalha de forma exaustiva a interação entre Apache, eventuais caches/proxies e todos os cabeçalhos de segurança.

## HSTS

HSTS não foi incluído automaticamente nesta migração. A diretiva cria estado persistente no navegador e deve ser habilitada somente após decisão específica sobre todos os requisitos HTTPS e subdomínios.
