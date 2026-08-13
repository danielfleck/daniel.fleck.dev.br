# Build do MkDocs

As fontes Markdown ficam em `mkdocs/docs/`. A configuração está em `mkdocs/mkdocs.yml` e a saída pública em `site/docs/`.

## Preparação

```bash
python -m pip install -e .
```

## Build

```bash
python scripts/build_docs.py
```

O script chama MkDocs em modo estrito, limpa a saída e normaliza o `sitemap.xml.gz` para tornar o build mais determinístico.

## Verificação

```bash
python scripts/build_docs.py --check
python scripts/validate_docs.py
```

O `--check` gera em diretório temporário e compara com `site/docs/`. Divergência significa que o build publicado/versionado está desatualizado.

## Não editar a saída

Qualquer correção de texto deve ser feita em `mkdocs/docs/`. Uma edição manual em `site/docs/` será perdida no próximo build.
