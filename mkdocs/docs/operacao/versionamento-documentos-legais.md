# Versionamento dos documentos legais

Política de Privacidade e Termos de Uso possuem ciclos independentes.

## Estado de referência atual

- Política de Privacidade: **Versão 5 — 13/08/2026 às 18:11 (BRT, UTC-3)**.
- Termos de Uso: **Versão 4 — 13/08/2026 às 18:11 (BRT, UTC-3)**.

A data/hora pública deve corresponder à publicação efetiva. Se um deploy falhar e a versão ainda não tiver chegado à produção, a evidência operacional deve registrar essa diferença.

## Alteração textual

Qualquer alteração de redação jurídica deve:

1. incrementar somente o documento efetivamente alterado;
2. registrar data/hora real e offset;
3. atualizar o comentário de manutenção;
4. acrescentar histórico público;
5. preservar entradas anteriores;
6. atualizar a governança correspondente;
7. gerar commit identificável.

## Alteração estrutural

Correção de `href`, canonical, navegação, layout ou diretório que não altera a redação jurídica não incrementa, por si só, a versão textual.

## Validação antes e depois

```bash
python scripts/rebuild.py
python scripts/build_docs.py
python scripts/validate.py
python scripts/validate_docs.py
python scripts/audit_network.py --all
```

Após o deploy, validar headers e rede de produção.
