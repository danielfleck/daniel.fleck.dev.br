# Matriz de fontes e evidências

> **Motivo do documento:** Evitar que suporte, inferência ou material secundário seja tratado como norma ou contrato.
> **Fundamento:** Princípios de responsabilização, transparência e demonstração de diligência; LGPD art. 6, X, e art. 50.
> **Regra de manutenção:** cada alteração relevante deve atualizar o motivo/fundamento correspondente e, quando afetar texto público, o racional da seção legal no mesmo commit.


## Classificações

| Classe | Exemplo | Como usar |
|---|---|---|
| Norma oficial | LGPD, Marco Civil, resolução ANPD, RFC | Pode fundamentar obrigação/requisito, respeitando escopo e vigência |
| Contrato do fornecedor | Contrato de E-mail/Hospedagem KingHost | Prova condições contratuais da relação, sujeito a versão/renovação |
| Política/documentação pública | Política LWSA, wiki KingHost | Prova o que o fornecedor publica; não prova necessariamente detalhe do plano |
| Comunicação escrita de suporte | WhatsApp KingHost | Evidência datada do atendimento; não elevar a contrato ou garantia universal |
| Observação técnica | build, header, auditoria Playwright | Prova o comportamento observado naquele estado/instante |
| Decisão interna | 90 dias máximos após encerramento de contato simples | Regra de governança, não lei |
| Pendência | país exato de toda cadeia do webmail | Não preencher com inferência |

## KingHost/e-mail

- **Localização física da cadeia do e-mail:** pendente. O suporte do plano não confirmou país/cidade.
- **SPF:** suporte e documentação convergem para `v=spf1 include:_spf.kinghost.net -all` para envio exclusivo pela infraestrutura KingHost.
- **DKIM:** documentação/suporte descrevem assinatura automática compartilhada com `dkim.kinghost.net`; não presumir alinhamento DMARC sem conferir mensagem real.
- **DMARC:** atual `p=none`; relatórios agregados exigem `rua`.
- **Antispam:** há controles do provedor, mas confirmar disponibilidade/configuração no plano.
- **Trash/spam:** contrato de e-mail prevê que mensagens nessas pastas podem ser apagadas após 20 dias.
- **Backup:** contrato/documentação descrevem backup diário mantido por até 7 dias.
- **Finalidades próprias:** contrato de e-mail e hospedagem contêm cláusula autorizando uso de dados/logs/IP e outros registros para melhoria/criação de sistemas/serviços.
- **Transferências:** Política de Privacidade LWSA admite que alguns dados podem ser transferidos a prestadores no exterior.

## Evidências restritas

Não publicar:
- captura integral de WhatsApp se contiver identificadores;
- cabeçalhos completos de e-mail real;
- DMARC failure report;
- log individual;
- documento de titular;
- formulário de incidente preenchido.

No Git/MkDocs público registrar apenas a conclusão e a classificação da evidência.

## Transporte e divulgação de vulnerabilidades

- **HSTS:** RFC 6797.
- **security.txt:** RFC 9116.
- **Redirect na KingHost:** documentação pública da Central de Ajuda, com regra distinta para Apache direto e Varnish.
- **mod_rewrite:** documentação Apache; query string é preservada por padrão quando a substituição não define outra query.

Essas fontes técnicas não transformam HSTS ou security.txt em obrigação legal específica deste site; são controles e boas práticas de segurança.
