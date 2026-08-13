# Visão geral da arquitetura

O `daniel.fleck.dev.br` é um **site estático multipágina**. O conteúdo entregue ao navegador é composto por HTML, CSS, JavaScript e arquivos estáticos. Não existe backend de conteúdo, CMS, banco de dados de posts ou API usada para montar páginas durante a navegação.

Cada post do Blog, item de Portfólio e registro da Base de Conhecimento possui URL própria e arquivo `index.html` próprio. Isso permite que o conteúdo exista como documento independente, com `<title>`, meta description, canonical e dados estruturados próprios.

Python participa exclusivamente do processo local de desenvolvimento. Os scripts:

1. criam esqueletos de conteúdo;
2. leem metadados gravados nos próprios HTMLs;
3. reconstróem índices e artefatos derivados;
4. validam estrutura, links e SEO;
5. geram a documentação MkDocs;
6. apoiam preview e empacotamento para revisão.

A raiz pública é `site/`. Scripts Python, templates, testes e fontes Markdown permanecem fora dessa raiz. A documentação MkDocs é exceção apenas no **resultado do build**, que é gravado em `site/docs/` como HTML/CSS/JS estático.

## Princípios técnicos

- uma URL real por conteúdo relevante;
- conteúdo útil disponível no HTML sem depender de `fetch()`;
- ausência de catálogo JSON mantido manualmente;
- metadados próximos do conteúdo que descrevem;
- áreas geradas claramente delimitadas;
- scripts locais idempotentes sempre que possível;
- validação antes do commit;
- redução de recursos externos automáticos;
- controle de versão de fontes e, quando adotado pelo projeto, dos artefatos publicados.

## Componentes

```text
conteúdo HTML individual
        │
        ├── CONTENT-META
        └── CONTENT-BODY
                │
                ▼
        scripts/rebuild.py
                │
   ┌────────────┼──────────────┐
   ▼            ▼              ▼
índices       tags           sitemap
SEO/JSON-LD   home           robots
```

O navegador recebe o resultado pronto. Nenhum script Python roda na hospedagem para atender uma requisição de visitante.
