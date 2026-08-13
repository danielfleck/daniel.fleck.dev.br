# Build e rebuild do site

`scripts/rebuild.py` reconstrói os artefatos derivados a partir das fontes já existentes no repositório.

## Execução

```bash
python scripts/rebuild.py
```

## O que é atualizado

- partials de navegação e rodapé;
- SEO e JSON-LD dos conteúdos;
- cabeçalhos gerados;
- índices de Blog, Portfólio e Erros;
- destaques da home;
- nuvem e páginas de tags;
- sitemap e robots;
- versionamento de assets quando previsto pelo script.

## Conferência sem gravar

```bash
python scripts/rebuild.py --check
```

O modo `--check` é adequado para validação/CI porque calcula se haveria mudanças sem alterar arquivos.

## Regra operacional

Após editar `CONTENT-META`, partials, CSS/JS globais ou lógica de geração, execute rebuild antes do commit. Não tente “consertar” manualmente todas as regiões geradas.
