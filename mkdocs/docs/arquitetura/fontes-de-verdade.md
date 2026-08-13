# Fontes de verdade

O projeto evita manter catálogos paralelos que precisem ser sincronizados manualmente.

## Conteúdo editorial

Para Blog, Portfólio e Erros e Soluções, a fonte de verdade é a própria página HTML individual:

```text
site/blog/<slug>/index.html
site/portfolio/<slug>/index.html
site/erros/<slug>/index.html
```

Cada página contém:

- `CONTENT-META`: título, resumo, slug, data, categoria, status, destaque e tags;
- `CONTENT-BODY`: texto editorial mantido pelo autor.

O `scripts/rebuild.py` lê os metadados e produz artefatos derivados. Portanto, não se mantém manualmente uma segunda lista de posts em JSON, JavaScript ou outro arquivo.

## Templates e componentes comuns

- navegação: `templates/partials/nav.html`;
- rodapé: `templates/partials/footer.html`;
- novo post: `templates/blog.html`;
- novo item de portfólio: `templates/portfolio.html`;
- novo erro conhecido: `templates/erro.html`.

## Documentação

A fonte da documentação técnica é `mkdocs/docs/`. `site/docs/` é build e pode ser reconstruído.

Documentos antigos como `SCRIPTS.md`, `docs/STRUCTURE.md`, `docs/AI-MAINTENANCE.md` e `docs/VALIDATION.md` não devem continuar como documentação canônica depois da migração, pois isso criaria duas fontes concorrentes.

## Governança e trabalho

Esta regra vale para o produto, não para gestão do projeto:

- Jira é fonte do trabalho e estado;
- Confluence é fonte de decisões, estratégia e governança interna;
- MkDocs é fonte do estado técnico resultante.

Quando um assunto tiver parte técnica e parte decisória, separe os registros em vez de copiar o mesmo documento integralmente para os dois locais.
