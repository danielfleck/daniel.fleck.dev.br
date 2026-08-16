# Auditoria de qualidade web — pendências de 15/08/2026

> **Motivo do documento:** impedir que achados automatizados ainda não revalidados sejam esquecidos ou marcados como resolvidos apenas porque houve uma release de privacidade/segurança.
>
> **Fundamento:** qualidade, acessibilidade, prevenção de regressões e rastreabilidade de evidência.
>
> **Regra de manutenção:** atualizar somente após repetir a medição e guardar evidência suficiente para confirmar correção ou falso positivo.

## Resultado recebido

O relatório de qualidade web informou pontuação **89/100 — Bom, com ajustes**.

## Achados ainda abertos

### 1. HTML fonte

O relatório encontrou **2 erros** no Nu HTML Checker.

**Estado:** aberto.

Não é possível corrigir com segurança apenas a partir do resumo; é necessário obter as mensagens/linhas exatas ou repetir o validador sobre a release atual.

### 2. Contraste

Foi apontada taxa de contraste insuficiente.

**Estado:** aberto.

Revalidar com axe/Lighthouse/WAVE e corrigir os pares específicos. Não alterar cores às cegas.

### 3. Erros no console

O navegador registrou erros.

**Estado:** aberto.

Repetir a auditoria depois dos novos scripts/modais e registrar:
- mensagem;
- URL;
- stack;
- navegador;
- página.

### 4. Áreas de toque

Foram apontadas áreas de toque pequenas ou muito próximas.

**Estado:** aberto.

Revalidar em viewport móvel e identificar elementos concretos antes de ajustar CSS.

### 5. llms.txt

A ausência foi descrita pelo próprio relatório como proposta comunitária, não erro.

**Decisão:** não criar `llms.txt` sem finalidade editorial e manutenção definida.

## Fechamento

Depois do deploy da release integrada:
1. repetir o mesmo teste;
2. executar Lighthouse/axe;
3. validar HTML;
4. registrar resultado;
5. somente então mudar o estado de cada item.
