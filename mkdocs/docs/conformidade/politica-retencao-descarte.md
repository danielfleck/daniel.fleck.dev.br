# Política de Retenção e Descarte

> **Motivo do documento:** Impedir retenção indefinida e documentar exceções de conservação.
> **Fundamento:** LGPD arts. 6, III, 15 e 16; exercício regular de direitos; regulamentação de incidentes quando aplicável.
> **Regra de manutenção:** cada alteração relevante deve atualizar o motivo/fundamento correspondente e, quando afetar texto público, o racional da seção legal no mesmo commit.


## Regra geral

A retenção decorre da finalidade e da necessidade. Não existe uma obrigação geral de guardar todas as mensagens por 90 dias, seis meses ou cinco anos.

## Matriz operacional

| Categoria | Regra padrão | Motivo |
|---|---|---|
| Spam/phishing sem valor probatório | excluir após triagem | minimização e redução de risco |
| Contato simples encerrado | excluir preferencialmente logo após encerramento; **máximo interno de 90 dias** sem motivo adicional | permitir follow-up curto sem retenção indefinida |
| Contato em andamento | enquanto ativo | finalidade ainda existe |
| Proposta/candidatura/projeto | enquanto necessário; definir data de revisão | contexto pode exigir continuidade |
| Mensagem com dado sensível desnecessário | restringir e eliminar assim que seguro | risco elevado e ausência de necessidade |
| Solicitação de titular | até conclusão + registro mínimo de accountability | comprovar atendimento sem conservar tudo |
| Incidente | registro do incidente conforme regulamentação; evidência pelo tempo necessário | obrigação específica |
| Disputa/ordem/preservação | `legal hold` documentado | exercício regular de direitos/obrigação |
| DMARC agregado | manter apenas o necessário para análise de autenticação; limpar periodicamente | relatório técnico |
| Backup do provedor | sujeito à mecânica/contrato do provedor | fora do controle direto do responsável |

## Limpeza trimestral

A cada revisão:
- caixa de entrada;
- enviados;
- lixeira;
- spam;
- arquivos exportados;
- downloads/anexos;
- celulares/computadores;
- pastas de DMARC;
- registros privados.

## KingHost

O contrato de e-mail informa que mensagens em `trash`, `lixeira` ou `spam` podem ser apagadas após 20 dias e que o backup é mantido por até 7 dias. Esses prazos são características do serviço do provedor, não a política de retenção definida pelo responsável.

## Legal hold

Nunca apagar automaticamente material sob retenção legal ativa. A retenção deve possuir:
- motivo;
- escopo;
- responsável;
- data inicial;
- próxima revisão;
- critério de encerramento.
