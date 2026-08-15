# Política Interna de Privacidade e Proteção de Dados

> **Motivo do documento:** Traduzir os princípios públicos em regras práticas de operação do site e da caixa postal.
> **Fundamento:** LGPD arts. 6, 15, 16, 37, 46, 47, 49 e 50; Resolução CD/ANPD nº 2/2022.
> **Regra de manutenção:** cada alteração relevante deve atualizar o motivo/fundamento correspondente e, quando afetar texto público, o racional da seção legal no mesmo commit.


**Aplicação:** site pessoal `daniel.fleck.dev.br` e e-mail público associado.  
**Responsável:** Daniel Rodrigo Fleck.  
**Canal público:** `/contato/` — `contato [arroba] fleck.dev.br`.

## Princípios operacionais

1. não criar coleta só porque tecnicamente é possível;
2. tratar apenas o necessário para finalidade concreta;
3. não usar e-mail público como credencial administrativa;
4. não enviar dados recebidos a IA, serviço externo ou ferramenta de terceiros sem necessidade e avaliação;
5. não copiar conteúdo de e-mail para Jira, Confluence, GitHub ou MkDocs quando um resumo sem dados pessoais for suficiente;
6. apagar dados quando a finalidade terminar, salvo exceção documentada;
7. aplicar `legal hold` somente com motivo, escopo e revisão;
8. guardar evidências sensíveis fora do repositório público;
9. usar autenticação forte e MFA onde disponível;
10. revisar fornecedor, normas e comportamento técnico periodicamente.

## Base de decisão

Para contato espontâneo, a base jurídica deve ser escolhida conforme a finalidade concreta. Não se usa consentimento de forma genérica apenas porque o remetente clicou em “abrir e-mail”.

## Dados recebidos por e-mail

Podem incluir remetente, nome informado, assunto, corpo, anexos, destinatários, data/hora e metadados que o provedor disponibilize.

Não presumir que o responsável tem acesso a IP de conexão, porta lógica, logs SMTP ou autenticação de infraestrutura.

## Dados sensíveis ou excessivos

Se chegarem sem necessidade:
1. não ampliar o compartilhamento;
2. não copiar para outros sistemas;
3. avaliar se é possível eliminar imediatamente;
4. se necessário responder, pedir que o remetente envie somente dados mínimos;
5. registrar apenas a decisão necessária, não o conteúdo sensível.

## Uso de IA

Não submeter mensagens reais, anexos, logs individualizados ou solicitações de titulares a serviços de IA externos sem base, necessidade, minimização e avaliação do fornecedor. Preferir dados fictícios/redigidos em estudos e prompts.

## Responsabilidade de fornecedor

KingHost/LWSA é avaliada por operação. O responsável mantém diligência sobre contrato, política, localização, subcontratados, retenção, segurança e cooperação para direitos.
