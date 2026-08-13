# Troubleshooting: webhook GitHub → KingHost

## Sintoma documentado

Após um push confirmado no GitHub, o site não refletiu a alteração. Na entrega do webhook apareceu a mensagem:

```text
failed to connect to host
```

## Diagnóstico responsável

A mensagem comprova que **aquela tentativa de entrega** não conseguiu conectar ao host configurado. Ela não identifica isoladamente se a causa estava no GitHub, KingHost, rede, disponibilidade momentânea ou configuração.

## Procedimento

1. confirmar que o commit/push esperado existe no GitHub;
2. abrir `Settings → Webhooks` no repositório;
3. selecionar o webhook relevante;
4. consultar `Recent deliveries`;
5. abrir a entrega associada ao push;
6. registrar a mensagem observada sem publicar IDs administrativos desnecessários;
7. quando adequado, executar `Redeliver`;
8. validar se a publicação ocorreu;
9. se a nova entrega falhar, coletar evidências adicionais antes de modificar credenciais ou configuração.

## Resultado do caso conhecido

No caso registrado, a mesma entrega funcionou após `Redeliver`, sem que uma alteração de código ou credencial fosse necessária. Por isso, a classificação segura é **falha pontual de entrega/conectividade**, não uma causa raiz atribuída a um fornecedor específico.

O relato editorial completo permanece em `/erros/`; este runbook guarda apenas o procedimento técnico reutilizável.
