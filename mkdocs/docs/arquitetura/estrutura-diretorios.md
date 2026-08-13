# Estrutura de diretórios

A separação entre raiz do projeto e raiz pública impede que scripts, testes e documentos internos sejam publicados apenas por existirem no repositório.

```text
/
├── README.md
├── pyproject.toml
├── .gitignore
├── .githooks/
│   └── pre-commit
├── templates/
│   ├── blog.html
│   ├── portfolio.html
│   ├── erro.html
│   └── partials/
├── scripts/
├── tests/
├── mkdocs/
│   ├── mkdocs.yml
│   └── docs/                 # fontes Markdown
└── site/                     # raiz pública
    ├── index.html
    ├── curriculo.html
    ├── 404.html
    ├── robots.txt
    ├── sitemap.xml
    ├── css/
    ├── js/
    ├── images/
    ├── blog/
    ├── portfolio/
    ├── erros/
    ├── tags/
    ├── ferramentas/
    ├── roadmap/
    ├── privacidade/
    ├── termos/
    └── docs/                 # build MkDocs
```

## Diretórios que são fonte

`templates/`, `scripts/`, `tests/` e `mkdocs/docs/` são fontes de desenvolvimento. Os conteúdos individuais dentro de `site/blog/`, `site/portfolio/` e `site/erros/` também são fontes autorais, pois guardam `CONTENT-META` e `CONTENT-BODY`.

## Diretórios e arquivos derivados

- `site/tags/` é gerado a partir das tags dos conteúdos;
- `site/sitemap.xml` e `site/robots.txt` são reconstruídos;
- regiões `GENERATED:*` nos HTMLs são derivadas;
- `site/docs/` é saída do MkDocs;
- `dist/` é artefato local e deve permanecer ignorado pelo Git;
- `*.egg-info/` é metadado de instalação Python e não deve ser versionado;
- `mkdocs/site/` é uma saída antiga/alternativa e não faz parte da arquitetura vigente.

## Regra de publicação

A publicação deve apontar para `site/` como raiz de conteúdo. Caso a hospedagem utilize outro diretório físico, o deploy deve copiar/sincronizar **o conteúdo de `site/`**, e não expor a raiz inteira do repositório como webroot.
