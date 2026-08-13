# Criar conteúdo

Um novo conteúdo deve ser criado por `scripts/create_content.py`, e não pela cópia manual de uma página antiga.

## Blog

```bash
python scripts/create_content.py blog
```

O assistente solicita título, resumo, data ISO, slug, categoria e tags. Ele cria `site/blog/<slug>/index.html` e executa o rebuild inicial.

Edite somente:

```html
<!-- CONTENT-BODY:START -->
...
<!-- CONTENT-BODY:END -->
```

## Portfólio

```bash
python scripts/create_content.py portfolio
```

## Erros e Soluções

```bash
python scripts/create_content.py erro
```

Diferencie fato, evidência, diagnóstico, hipótese, solução e resultado. Não marque como resolvido sem confirmação.

## Depois da edição

```bash
python scripts/rebuild.py
python scripts/build_docs.py --check
python scripts/validate.py
python scripts/validate_docs.py
python scripts/audit_network.py --all
python scripts/serve.py
```

A sequência operacional completa e canônica está em `SCRIPTS.md` na raiz.
