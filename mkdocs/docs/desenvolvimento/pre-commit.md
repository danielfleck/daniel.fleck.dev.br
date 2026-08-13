# Pre-commit

O repositório usa `.githooks/pre-commit` para impedir commits em que artefatos derivados estejam inconsistentes com as fontes.

## Instalação

```bash
python scripts/install_hooks.py
```

A instalação precisa ser repetida depois de um novo clone porque `core.hooksPath` é uma configuração local.

## Fluxo

O hook procura o Python da `.venv` e executa, em ordem:

1. `scripts/rebuild.py --hook`;
2. `scripts/build_docs.py --hook`;
3. `scripts/validate.py`;
4. `scripts/validate_docs.py`.

Se o rebuild ou o build do MkDocs alterar arquivos, o commit é interrompido. O autor deve revisar as diferenças e executar conscientemente:

```bash
git status
git diff
git add -A
git commit -m "Descrição"
```

O hook **não** adiciona arquivos automaticamente. Essa decisão preserva revisão humana sobre arquivos gerados.

## Não usar como substituto de revisão

Um hook aprovado não prova que o conteúdo está correto. Antes de alterações importantes, execute preview local e leia `git diff`.
