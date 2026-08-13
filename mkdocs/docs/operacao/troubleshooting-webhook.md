# Troubleshooting: webhook GitHub → KingHost

Este documento registra sintomas observados sem converter hipótese em causa raiz.

## Caso 1 — `failed to connect to host`

Em caso anterior, após push confirmado no GitHub, uma entrega apresentou:

```text
failed to connect to host
```

A mesma entrega funcionou após `Redeliver`. A classificação segura permanece: falha pontual de entrega/conectividade, sem atribuição conclusiva de causa.

## Caso 2 — `unsupported reference string`

Em 13/08/2026, após novo push, a integração retornou:

```json
{"status":"fail","message":"unsupported reference string","transaction_id":null,"queue_id":null}
```

Esse retorno prova a rejeição daquela tentativa, mas não informa sozinho qual formato de referência foi recusado.

O fato de `transaction_id` e `queue_id` estarem nulos é compatível com rejeição antes de uma operação normal de deploy entrar em fila, mas isso deve ser tratado como **inferência**, não como confirmação da arquitetura interna da KingHost.

## Verificações para `unsupported reference string`

Antes de alterar código do site:

```bash
git status
git branch --show-current
git log -1 --oneline
git remote -v
git ls-remote --heads origin
git rev-parse HEAD
git rev-parse origin/main
```

Confirmar no painel da hospedagem que a referência de publicação é a branch simples esperada, normalmente:

```text
main
```

e não uma URL, `origin/main` ou outra representação de ref, salvo instrução explícita do provedor.

## Procedimento geral

1. confirmar que o commit esperado existe no GitHub;
2. confirmar a branch efetivamente enviada;
3. confirmar a branch configurada no painel KingHost;
4. abrir a entrega do webhook e preservar a mensagem exata;
5. não alterar `.htaccess`, CSP ou MkDocs apenas por erro de parsing da referência;
6. se a integração continuar falhando em `main`, abrir chamado com a KingHost anexando a resposta exata do webhook;
7. somente após deploy bem-sucedido executar as validações pós-publicação.

IDs administrativos, URLs secretas de webhook e credenciais não devem ser publicados nesta documentação.
