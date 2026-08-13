# Criar conteúdo

Um novo conteúdo deve ser criado por `scripts/create_content.py`, e não pela cópia manual de uma página antiga.

## Blog

```bash
python scripts/create_content.py blog
```

O assistente solicita:

1. título;
2. resumo;
3. data ISO;
4. slug;
5. categoria;
6. tags.

Ele cria `site/blog/<slug>/index.html` a partir de `templates/blog.html` e executa o rebuild.

Depois, edite somente:

```html
<!-- CONTENT-BODY:START -->
...
<!-- CONTENT-BODY:END -->
```

## Portfólio

```bash
python scripts/create_content.py portfolio
```

Além dos metadados comuns, o script pergunta se o item deve aparecer nos destaques da home.

## Erros e Soluções

```bash
python scripts/create_content.py erro
```

O template de erro deve separar fato observado, evidência, diagnóstico, hipótese, solução e resultado. Não marque como resolvido se a correção ainda não foi validada.

## Depois da edição

```bash
python scripts/rebuild.py
python scripts/build_docs.py --check
python scripts/validate.py
python scripts/validate_docs.py
python scripts/serve.py
```

Não é necessário cadastrar manualmente o novo conteúdo em JSON, lista JavaScript, sitemap, nuvem de tags ou página de tag. Esses artefatos são derivados de `CONTENT-META`.
