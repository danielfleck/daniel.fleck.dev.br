# CONTENT-META

`CONTENT-META` é o bloco de metadados embutido no próprio HTML das páginas de conteúdo. Ele evita um catálogo JSON paralelo e mantém as informações de indexação próximas ao texto que descrevem.

Exemplo conceitual:

```text
<!-- CONTENT-META
type: blog
slug: exemplo
title: Título do conteúdo
summary: Resumo objetivo
published: 2026-08-13
display_date: 13 Ago 2026
category: Técnico
status:
featured: false
tags: Python | GitHub | Site Estático
-->
```

## Campos

- `type`: `blog`, `portfolio` ou tipo de erro reconhecido pelos scripts;
- `slug`: identificador usado na URL;
- `title`: título principal;
- `summary`: resumo usado em listagens e meta description;
- `published`: data ISO;
- `display_date`: data exibida na interface;
- `category`: categoria editorial;
- `status`: usado especialmente em erros;
- `featured`: controla destaque do portfólio quando suportado;
- `tags`: lista separada pelo delimitador definido pelo projeto.

## Regras

- não inserir quebras de linha em campos de linha única;
- não usar `-->` dentro dos valores;
- manter tags com capitalização consistente;
- não alterar slug publicado sem estratégia de redirecionamento;
- executar rebuild após qualquer alteração de metadado.

O cabeçalho visível, SEO, JSON-LD e índices são derivados desse bloco e não devem ser mantidos manualmente em paralelo.
