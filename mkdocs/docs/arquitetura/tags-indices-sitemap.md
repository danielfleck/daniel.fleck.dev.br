# Tags, índices e sitemap

Tags são propriedades do próprio conteúdo e ficam em `CONTENT-META`. Durante o rebuild, as páginas de Blog, Portfólio e Erros e Soluções são percorridas e suas tags são agregadas.

## Páginas de tag

Para cada tag é criada uma página HTML estática em:

```text
site/tags/<slug-da-tag>/index.html
```

A página agrupa conteúdos por tipo e contém links HTML convencionais para suas URLs canônicas. Não há consulta a banco, API ou JSON no navegador.

## Nuvem de tags

A nuvem é produzida no build. A frequência é calculada a partir das ocorrências reais em `CONTENT-META`. O tamanho visual varia de **11 a 20 px**:

- menor frequência → tamanho próximo de 11 px;
- maior frequência → tamanho próximo de 20 px;
- mesma frequência → mesmo tamanho.

A nuvem não precisa recalcular nada no navegador.

## Índices

O rebuild atualiza:

- `site/blog/index.html`;
- `site/portfolio/index.html`;
- `site/erros/index.html`;
- destaques e conteúdos recentes da home.

## Sitemap e robots

O mesmo inventário de páginas é utilizado para gerar `site/sitemap.xml`. O `robots.txt` aponta para o sitemap principal e para o sitemap da documentação em `/docs/`.

Páginas de tag geradas que deixam de possuir membros devem ser removidas pelo rebuild, evitando URLs órfãs.
