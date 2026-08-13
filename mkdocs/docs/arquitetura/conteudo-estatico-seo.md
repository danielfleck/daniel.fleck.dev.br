# Conteúdo estático e SEO

A migração para arquitetura multipágina substituiu a dependência de hashes/sections por URLs reais para os conteúdos principais. Cada página relevante pode ser descoberta e indexada de forma independente.

## Requisitos por página de conteúdo

Cada post, projeto ou erro conhecido deve possuir:

- uma URL estável baseada no slug;
- exatamente um `<title>`;
- meta description;
- canonical único;
- um `<h1>`;
- Open Graph básico;
- JSON-LD apropriado ao tipo;
- links HTML convencionais para navegação e tags.

O rebuild usa:

- `BlogPosting` para Blog;
- `CreativeWork` para Portfólio;
- `TechArticle` para Erros e Soluções.

## Conteúdo não dependente de JavaScript

Listagens, títulos, resumos e páginas de tags são gravados no HTML. JavaScript permanece apenas para interações locais e compatibilidade, não para buscar o texto principal do conteúdo.

Essa regra deve ser preservada. Não introduza `fetch()` de catálogo de posts, renderização client-side obrigatória ou dependência de API apenas para montar conteúdo que pode estar pronto no HTML.

## Slugs e URLs

O slug é parte da URL pública e deve ser tratado como identificador estável. Evite alterar slugs publicados. Se uma alteração for indispensável, planeje redirecionamento permanente e atualização de links/sitemap.

## Validação

`scripts/validate.py` confere metadados e consistência das páginas próprias do site. O build MkDocs possui validação separada, pois o Material for MkDocs gera uma estrutura HTML diferente.
