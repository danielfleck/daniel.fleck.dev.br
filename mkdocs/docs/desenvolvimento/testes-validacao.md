# Testes e validação

As validações são complementares.

## Testes unitários

```bash
python -m unittest discover -s tests -v
```

## Site principal e coerência do projeto

```bash
python scripts/validate.py
```

Verifica, entre outros:
- conteúdo e metadados;
- links, SEO e sitemap;
- documentos jurídicos e versões esperadas;
- links de Privacidade e Termos na página inicial;
- ausência de `frame-ancestors` em CSP por `<meta>`;
- configuração do MkDocs;
- modelo documental sem `*-resumo.md` no MkDocs;
- `.htaccess`;
- hooks;
- estado do rebuild e do build da documentação.

## Material for MkDocs

```bash
python scripts/validate_docs.py
```

Valida a saída específica de `site/docs/`, inclusive CSS, referências locais e carregamentos externos.

## Rede em runtime

```bash
python scripts/audit_network.py --all
```

Este é o teste que detecta `fetch()`, XHR, WebSocket e outras requisições criadas dinamicamente por JavaScript.

## Produção

```bash
python scripts/validate.py \
  --production-url https://daniel.fleck.dev.br \
  --network

python scripts/validate_docs.py \
  --production-url https://daniel.fleck.dev.br/docs/
```

A publicação somente deve ser considerada tecnicamente confirmada depois da validação da resposta HTTP final.
