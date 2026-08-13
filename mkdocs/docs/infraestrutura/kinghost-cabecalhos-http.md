# KingHost e cabeçalhos HTTP

## Atendimento de 13/08/2026

Foi solicitado ao suporte esclarecimento sobre uso de `mod_headers`, herança de `.htaccess` e possíveis camadas intermediárias.

O atendimento informou que:

- o ambiente Linux permite diretivas como `Header always set` em `.htaccess`;
- a configuração pode ser aplicada a respostas de HTML estático atendidas pelo Apache;
- regras da raiz são normalmente herdadas por subdiretórios, salvo contexto mais específico;
- a documentação disponível não registra restrição específica de plano para CSP;
- a infraestrutura pode envolver Varnish/Magic Cache e referências a Nginx em alguns recursos;
- a documentação disponível não permite afirmar categoricamente que nenhuma camada intermediária alterará cabeçalhos de segurança;
- não foi confirmada uma precedência exaustiva entre headers definidos pelo cliente e eventuais camadas intermediárias;
- a recomendação prática foi publicar, limpar cache quando aplicável e validar os cabeçalhos recebidos por DevTools ou `curl`.

## Consequência arquitetural

A configuração do repositório define os headers, mas **o estado de produção somente é considerado comprovado depois da inspeção da resposta HTTP final**.

O registro integral do atendimento é mantido fora do site, em arquivo restrito.

## Validação

```bash
python scripts/validate.py --production-url https://daniel.fleck.dev.br
```

ou:

```bash
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/docs/
```
