# Pre-commit e pre-push

O repositório usa hooks versionados em `.githooks/`.

## Instalação

```bash
python scripts/install_hooks.py
```

## Pre-commit

O `git commit` executa, em ordem:

1. `scripts/rebuild.py --hook`;
2. `scripts/build_docs.py --hook`;
3. `scripts/validate.py`;
4. `scripts/validate_docs.py`.

Se `rebuild.py` ou `build_docs.py` modificar artefatos, o commit é interrompido para revisão.

```bash
git status
git diff
git add -A
git commit -m "Descrição"
```

## Pre-push

O `git push` executa:

```bash
python scripts/audit_network.py --all
```

A auditoria abre o site gerado em Chromium headless e bloqueia o push se houver erro de navegação ou tentativa de conexão para host externo não autorizado.

## Limite

Hook aprovado não substitui leitura do `git diff`, inspeção visual nem validação pós-deploy.
