# Segurança do e-mail — SPF, DKIM, DMARC e operação

> **Motivo do documento:** Reduzir spoofing e permitir evolução controlada do DMARC sem bloquear e-mails legítimos ou criar coleta excessiva.
> **Fundamento:** LGPD art. 46 como dever geral de segurança; RFC 7208, RFC 6376, RFC 9989, RFC 9990 e RFC 9991; documentação KingHost.
> **Regra de manutenção:** cada alteração relevante deve atualizar o motivo/fundamento correspondente e, quando afetar texto público, o racional da seção legal no mesmo commit.


## Estado consolidado em 15/08/2026

### SPF

Registro confirmado na zona DNS:

```text
v=spf1 include:_spf.kinghost.net -all
```

Adequado ao cenário informado de envio exclusivamente pela KingHost. Não criar segundo registro SPF.

### DKIM

A KingHost informa que mensagens enviadas pela infraestrutura são assinadas automaticamente e que, para clientes, o domínio de assinatura padrão é:

```text
dkim.kinghost.net
```

A documentação informa que não há DKIM exclusivo por domínio de cliente como recurso padrão; um DKIM próprio pode depender de serviço externo.

### DMARC

Registro atual:

```text
v=DMARC1; p=none;
```

É válido como política sem enforcement, porém não contém `rua`. Sem `rua`, o domínio não solicita relatórios agregados aos receivers.

## Próxima etapa recomendada

1. criar caixa/alias dedicada `dmarc-reports [arroba] fleck.dev.br`;
2. não usar a caixa de contato para relatórios;
3. depois de a caixa estar pronta, considerar:

```text
v=DMARC1; p=none; rua=mailto:dmarc-reports@fleck.dev.br;
```

4. coletar relatórios por pelo menos um ciclo representativo;
5. usar `scripts/parse_dmarc_report.py`;
6. enviar mensagens de teste a provedores diferentes e usar `scripts/check_email_auth.py` sobre cabeçalhos salvos localmente;
7. somente depois avaliar `p=quarantine`;
8. somente depois de nova observação avaliar `p=reject`.

## Por que não avançar agora para `reject`

DMARC depende de autenticação **alinhada**. A assinatura DKIM compartilhada descrita pela KingHost usa um domínio diferente de `fleck.dev.br`; ela, sozinha, não deve ser tomada como prova de alinhamento. SPF pode fornecer alinhamento dependendo do envelope usado efetivamente.

Portanto, a decisão precisa ser baseada no `Authentication-Results` de mensagens reais e nos relatórios agregados.

## RFC atual

A série DMARC atual de referência é:
- RFC 9989 — mecanismo/política DMARC;
- RFC 9990 — relatórios agregados;
- RFC 9991 — relatórios de falha.

Esses documentos substituem/obsoletam o uso do RFC 7489 como referência principal.

## `rua` x `ruf`

Usar inicialmente apenas **`rua`**.

Não configurar `ruf` nesta etapa. Relatórios de falha podem conter cabeçalhos e até conteúdo de mensagens e podem gerar risco de privacidade e volume operacional.

## SPF e DKIM não bloqueiam spam recebido

SPF/DKIM/DMARC ajudam a autenticar remetentes/domínios e proteger a reputação do domínio. Eles não são mecanismo suficiente contra alguém que envia milhares de mensagens **para** `contato@...`.

Para inbound abuse usar controles do provedor, filtros, treinamento antispam, bloqueios, quotas e suporte.
