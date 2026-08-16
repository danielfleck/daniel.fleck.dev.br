# Procedimento — resposta a incidentes de segurança

> **Motivo do documento:** Definir contenção, avaliação, comunicação e registro para eventos que envolvam dados pessoais.
> **Fundamento:** LGPD arts. 46 e 48; Resolução CD/ANPD nº 15/2024 e regime diferenciado aplicável ao pequeno porte.
> **Regra de manutenção:** cada alteração relevante deve atualizar o motivo/fundamento correspondente e, quando afetar texto público, o racional da seção legal no mesmo commit.


## Exemplos de gatilho

- invasão/comprometimento do webmail;
- vazamento de senha;
- acesso não autorizado ao painel;
- publicação acidental de dado pessoal;
- exposição de `/stats`;
- comprometimento de DNS;
- malware em dispositivo com sessão ativa;
- perda de dispositivo;
- mail-bombing com indisponibilidade relevante;
- exposição acidental de relatório DMARC ou `.eml`.

## Fase 1 — conter

1. interromper acesso indevido;
2. revogar sessões quando possível;
3. trocar credenciais comprometidas;
4. proteger DNS/conta;
5. acionar KingHost se infraestrutura estiver envolvida;
6. não destruir evidência necessária para entender o evento.

## Fase 2 — entender

Registrar:
- quando ocorreu/foi detectado;
- sistema;
- dados pessoais afetados;
- quantidade aproximada;
- titulares;
- existência de dados sensíveis, financeiros, autenticação, menores ou sigilo;
- causa provável;
- medidas já adotadas.

## Fase 3 — avaliar comunicação

A comunicação à ANPD/titulares não é automática para todo evento. Verificar se o incidente pode acarretar **risco ou dano relevante** e a regulamentação vigente.

A regra geral da Resolução nº 15/2024 estabelece prazo de três dias úteis para incidentes comunicáveis. A Resolução nº 2/2022 contém tratamento diferenciado para agentes de pequeno porte. Confirmar o prazo aplicável no momento do incidente.

Se faltarem informações, considerar comunicação preliminar/complementar conforme a regulamentação.

## Fase 4 — registrar

O registro de incidente com dados pessoais deve ser preservado pelo prazo regulamentar aplicável; a Resolução nº 15/2024 estabelece no mínimo cinco anos.

O registro preenchido é **privado**.

## Fase 5 — aprender

- causa raiz;
- controle que falhou;
- correção;
- teste;
- atualização de documentação;
- revisão de fornecedor;
- data de encerramento.
