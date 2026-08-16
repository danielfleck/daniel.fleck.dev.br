# Diligência pendente — KingHost/LWSA

> **Motivo do documento:** manter visíveis as questões técnicas e de privacidade que ainda dependem de confirmação do fornecedor, evitando que uma inferência seja promovida a fato.
>
> **Fundamento:** responsabilização, transparência, segurança, diligência de fornecedor e documentação de limitações.
>
> **Regra de manutenção:** quando uma resposta formal for obtida, registrar data, natureza da evidência e conclusão; a evidência integral deve ficar restrita quando contiver dados pessoais ou informações desnecessárias à publicação.

## 1. Transporte web

Confirmar:
- Varnish/proxy ativo;
- presença e confiabilidade de `X-Forwarded-Proto`;
- regra recomendada para HTTPS;
- suporte efetivo a HSTS via `Header always set`;
- passagem do HSTS por cache/proxy;
- herança do `.htaccess` da raiz em `/docs/`;
- purga de cache;
- renovação automática do certificado.

## 2. security.txt

Confirmar:
- publicação de `/.well-known/`;
- `Content-Type: text/plain; charset=utf-8`;
- ausência de bloqueio/rewrite específico nesse caminho.

## 3. Logs

Confirmar formalmente:
- o que significa a retenção de 90 dias informada pelo suporte;
- campos;
- IP;
- porta lógica quando disponível;
- backups;
- acesso do cliente;
- cooperação em direitos dos titulares/ordens.

## 4. `/stats`

Confirmar:
- origem dos dados;
- retenção;
- rate limiting;
- bloqueio de tentativas;
- relação com `/varnish-stats/`.

## 5. Privacidade e contratos

Confirmar:
- alcance real das finalidades próprias previstas contratualmente;
- documentação de papéis por operação;
- eventual DPA/Contrato de Transferência de Dados aplicável.

## 6. E-mail

Confirmar:
- localização da cadeia;
- backups;
- antispam;
- subprocessadores;
- eventual acesso/transferência internacional;
- alinhamento SPF/DKIM/DMARC;
- mecanismos contra flooding/mail-bombing.

## Evidência

Classificar cada resposta como:
- contrato;
- política/documentação pública;
- ticket/e-mail;
- WhatsApp/suporte;
- observação técnica.

Nunca registrar como “garantia contratual” aquilo que foi apenas informado por atendimento.
