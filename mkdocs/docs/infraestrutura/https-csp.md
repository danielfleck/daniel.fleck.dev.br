# HTTPS e Content Security Policy

O site usa HTTPS e uma política CSP restritiva para reduzir carregamentos automáticos e comportamentos não necessários.

## CSP em `<meta>`

A política entregue por `<meta http-equiv="Content-Security-Policy">` pode controlar várias diretivas, mas possui limitações. Em particular, `frame-ancestors` **não é aplicado quando aparece numa política entregue por `meta`**. Por isso, essa diretiva não deve permanecer no HTML como se fornecesse proteção anti-framing.

A proteção por `frame-ancestors` deve ser configurada como **header HTTP** no servidor/proxy que entrega a resposta, ou deve ser adotado outro header compatível conforme a decisão técnica testada.

## Estado de migração

O pacote de migração remove a diretiva ineficaz do CSP em `meta`, mas não presume que a proteção HTTP já esteja configurada na KingHost. A tarefa só pode ser considerada concluída depois de observar o header efetivamente recebido pelo navegador/cliente HTTP.

## Atenção ao `/docs/`

O Material for MkDocs gera JavaScript inline. Uma CSP HTTP que simplesmente replique `script-src 'self'` pode quebrar busca e interface da documentação. Portanto:

1. testar política no site principal;
2. testar `/docs/` separadamente;
3. preferir uma configuração que não exija relaxar desnecessariamente o site principal;
4. confirmar os headers em produção;
5. registrar a configuração resultante depois do teste.

## Validação opcional

```bash
python scripts/validate_docs.py --production-url https://daniel.fleck.dev.br/docs/
```

Esse comando observa headers, mas a validação final deve incluir inspeção real do site após o deploy.
