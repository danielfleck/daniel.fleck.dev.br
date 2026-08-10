# Estrutura do site

O conteúdo publicado continua 100% estático. Python é ferramenta local de criação, rebuild e validação.

```text
/
├── index.html                 # home/hub
├── curriculo.html             # currículo independente
├── 404.html
├── robots.txt
├── sitemap.xml                # gerado
├── css/                       # estilos compartilhados
├── js/main.js                 # apenas interações locais/compatibilidade de hashes antigos
├── images/
├── blog/
│   ├── index.html             # índice gerado a partir de CONTENT-META
│   └── <slug>/index.html      # 1 arquivo por post
├── portfolio/
│   ├── index.html
│   └── <slug>/index.html      # 1 arquivo por item
├── erros/
│   ├── index.html
│   └── <slug>/index.html      # 1 registro por problema/solução
├── tags/
│   ├── index.html
│   └── <tag>/index.html       # páginas geradas
├── roadmap/index.html
├── ferramentas/index.html
├── privacidade/index.html
├── termos/index.html
├── templates/
│   ├── blog.html
│   ├── portfolio.html
│   ├── erro.html
│   └── partials/              # navegação e rodapé
├── scripts/
│   ├── create_content.py
│   ├── rebuild.py
│   ├── validate.py
│   ├── serve.py
│   ├── install_hooks.py
│   └── package_for_ai.py
├── tests/
├── .githooks/pre-commit
└── docs/AI-MAINTENANCE.md
```

## Fontes de verdade

- Post individual: `CONTENT-META` + `CONTENT-BODY` no próprio HTML.
- Navegação/rodapé: `templates/partials/`.
- Listagens, tags, sitemap e SEO de conteúdos: gerados por `scripts/rebuild.py`.
- Política e Termos: páginas jurídicas próprias, com controle de versão indicado nos comentários de cada arquivo.

## Não editar manualmente

Regiões `GENERATED:*`, páginas individuais em `tags/` e `sitemap.xml`.
