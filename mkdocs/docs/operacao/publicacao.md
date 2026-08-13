# Publicação

A publicação parte de um repositório local validado e chega ao ambiente KingHost por integração com GitHub.

## Antes do commit

```bash
python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/validate_docs.py
python -m unittest discover -s tests -v
```

Faça preview se a alteração tiver impacto visual.

## Commit e push

```bash
git status
git diff
git add -A
git commit -m "Descrição objetiva"
git push
```

O pre-commit pode interromper o commit se gerar artefatos novos. Revise, adicione novamente e repita.

## Depois do push

Não presuma que push bem-sucedido significa deploy concluído. Valide o site publicado e, quando necessário, o histórico de webhook.

## Escopo de publicação

O servidor deve expor a raiz pública correspondente a `site/`. Arquivos de desenvolvimento e backups não devem ficar acessíveis por HTTP apenas porque fazem parte do repositório.
