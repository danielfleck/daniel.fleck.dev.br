# Versionamento dos documentos legais

Política de Privacidade e Termos de Uso possuem ciclos de versão independentes.

## Estado de referência desta migração

- Política de Privacidade: **Versão 4**, publicada em 10/08/2026 às 00:58 (BRT, UTC-3).
- Termos de Uso: **Versão 3**, publicada no mesmo marco da revisão correspondente.

## Alteração textual

Qualquer alteração de redação do documento jurídico deve:

1. incrementar a versão do documento efetivamente alterado;
2. registrar data/hora real de publicação em `America/Sao_Paulo` e offset UTC;
3. atualizar comentário de manutenção;
4. acrescentar histórico público sem apagar entradas anteriores;
5. registrar a mudança na governança interna;
6. gerar commit identificável.

Termos e Privacidade são independentes: alterar um não incrementa automaticamente o outro.

## Alteração estrutural

Mudanças que não alteram a redação jurídica — por exemplo, correção de `href`, reorganização de diretório, canonical ou navegação — não incrementam por si mesmas a versão textual.

A correção do antigo link SPA de Privacidade dentro dos Termos é classificada nesta categoria, desde que apenas o atributo de navegação seja modificado.

## Fonte da justificativa

Este documento descreve **como publicar tecnicamente** uma alteração jurídica. O motivo, análise, evidências e avaliação de impacto pertencem ao registro interno de governança.
