# Runbook técnico de incidentes

Este documento descreve a resposta **técnica**. A decisão jurídica sobre comunicação à ANPD, titulares ou autoridades é tratada pela governança aplicável.

## 1. Detectar e registrar

Registre data/hora do conhecimento, sintoma, componente afetado e fonte da detecção. Não copie dados pessoais além do necessário para investigar.

## 2. Conter

Exemplos conforme o caso:

- desativar credencial/token suspeito;
- retirar temporariamente conteúdo comprometido;
- desativar serviço administrativo;
- reverter deploy malicioso;
- acionar o provedor.

## 3. Preservar evidências mínimas

Preservar commits, timestamps, mensagens de erro, protocolos e registros necessários sem criar uma coleta ampla de visitantes. Quando registros estiverem apenas com o provedor, agir rapidamente se houver necessidade de preservação.

## 4. Investigar

Distinguir:

- fato observado;
- hipótese;
- causa comprovada;
- medida de contenção;
- correção definitiva.

## 5. Corrigir e validar

Aplicar a correção, executar testes, validar o ambiente publicado e verificar se não houve regressão.

## 6. Escalonar governança

Se houver dados pessoais envolvidos, encaminhar a avaliação para o procedimento interno de incidentes, que considera risco/dano, registros obrigatórios, prazos regulatórios e eventual comunicação.

## 7. Retrospectiva

Depois do encerramento, registrar causa, impacto, medidas e ações preventivas. Se o caso for publicável e tecnicamente útil, criar registro sanitizado em Erros e Soluções sem expor pessoas, IPs ou segredos.
