# HTTPS e Content Security Policy

O site usa HTTPS e políticas CSP distintas para o site principal e para `/docs/`.

## Site principal

A CSP de recursos permanece em `<meta http-equiv="Content-Security-Policy">` para as diretivas compatíveis. `frame-ancestors` não permanece no `<meta>` porque a proteção anti-framing precisa ser entregue por cabeçalho HTTP.

`site/.htaccess` define:

```apache
Header always set Content-Security-Policy "frame-ancestors 'none'"
Header always set X-Frame-Options "DENY"
Header always set Referrer-Policy "no-referrer"
Header always set X-Content-Type-Options "nosniff"
```

## `/docs/`

Material for MkDocs utiliza JavaScript inline de inicialização. Por isso `/docs/` recebe uma CSP própria, cuja fonte é `mkdocs/.htaccess` e cuja cópia pública é `site/docs/.htaccess`.

A política inclui:

```text
script-src 'self' 'unsafe-inline'
connect-src 'self'
frame-ancestors 'none'
```

`connect-src 'self'` impede conexões programáticas para terceiros sem impedir links `<a>` acionados pelo visitante.

## KingHost

O suporte confirmou em 13/08/2026 o uso de `Header always set` no ambiente Linux e a aplicação normal a HTML estático/subdiretórios. Não foi documentada de forma exaustiva a precedência de eventuais camadas intermediárias.

Portanto o estado configurado no Git não é, sozinho, prova do header final.

## Validação

```bash
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/docs/

python scripts/validate.py \
  --production-url https://daniel.fleck.dev.br \
  --network

python scripts/validate_docs.py \
  --production-url https://daniel.fleck.dev.br/docs/
```

HSTS continua fora desta configuração até decisão específica sobre seu alcance e persistência.
