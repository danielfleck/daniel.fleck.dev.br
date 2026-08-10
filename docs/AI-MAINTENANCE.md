# Instruções para edição por IA

## Regra principal

O site publicado é **100% estático**. Python existe apenas como ferramenta local de criação, rebuild e validação. Não adicionar backend, CMS, banco de dados ou carregamento dinâmico de conteúdo sem solicitação expressa.

## Onde editar

- Conteúdo de Blog: `blog/<slug>/index.html`.
- Portfólio: `portfolio/<slug>/index.html`.
- Erros e Soluções: `erros/<slug>/index.html`.
- Dentro dessas páginas, `CONTENT-META` é a fonte dos metadados e `CONTENT-BODY` é a fonte do texto.
- Navegação/rodapé: `templates/partials/`.
- Layout: `css/`.
- Configuração global: `scripts/site_config.py`.
- **Nunca** editar manualmente áreas entre `GENERATED:*`.

## Depois de qualquer alteração

```bash
python scripts/rebuild.py
python scripts/validate.py
python -m unittest discover -s tests
```

## Regra especial para problemas técnicos

Ao analisar um pedido de edição, verificar se o usuário descreveu problema real identificado e resolvido. Se já existir registro equivalente em `erros/`, editar o existente. Se for novo e houver informação suficiente, criar com `python scripts/create_content.py erro`. Se faltarem contexto, mensagem exata, evidência, ação aplicada ou confirmação do resultado, perguntar antes de inventar.

## Documentos jurídicos

`privacidade/index.html` e `termos/index.html` possuem comentários próprios de versionamento. Qualquer alteração textual exige seguir a regra indicada na própria página.

## Auditoria por outra IA

Para revisar conteúdo renderizado, informe a URL do site **e** `https://daniel.fleck.dev.br/sitemap.xml`; o sitemap funciona como manifesto das páginas públicas. Para revisar código, informe o repositório `https://github.com/danielfleck/daniel.fleck.dev.br` quando a IA possuir acesso web ao GitHub. Como nem toda IA consegue varrer recursivamente um repositório/site, a forma mais confiável é executar:

```bash
python scripts/package_for_ai.py
```

e enviar `dist/site-for-ai.zip` em uma única conversa. Assim a IA recebe todos os HTML, CSS, JS, templates, scripts e instruções sem que você tenha de anexar dezenas de arquivos manualmente.
