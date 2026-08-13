# Rollback e restauração

A estratégia primária de recuperação é baseada no histórico Git e na capacidade de reconstruir os artefatos derivados.

## Rollback de uma alteração recente

1. identificar o commit que introduziu o problema;
2. avaliar se o histórico é compartilhado/publicado;
3. preferir `git revert` para desfazer um commit já publicado, preservando rastreabilidade;
4. executar rebuild e build do MkDocs;
5. validar;
6. publicar o novo commit;
7. executar verificação pós-deploy.

Exemplo:

```bash
git log --oneline
git revert <sha>
python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/validate_docs.py
git push
```

## Restauração local

Um clone limpo deve conseguir reconstruir o projeto com:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python scripts/rebuild.py
python scripts/build_docs.py
```

## Backups do provedor

Backups da hospedagem são recurso complementar. Não devem ser a única forma de restaurar código, documentação técnica ou histórico jurídico próprio.

## Documentos internos

Backups privados da governança Confluence devem permanecer fora da raiz pública e em local independente do próprio Confluence, para reduzir risco de perda por desativação de conta/espaço.
