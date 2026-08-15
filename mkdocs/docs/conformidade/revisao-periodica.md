# Revisão periódica de conformidade

> **Motivo do documento:** Evitar que documentos permaneçam formalmente bonitos, mas tecnicamente ou juridicamente desatualizados.
> **Fundamento:** LGPD art. 50; responsabilização, prevenção e governança.
> **Regra de manutenção:** cada alteração relevante deve atualizar o motivo/fundamento correspondente e, quando afetar texto público, o racional da seção legal no mesmo commit.


## Cadência

### Em todo commit

O `pre-commit` executa `scripts/compliance_gate.py`. O objetivo é lembrar que o commit pode alterar:
- coleta;
- links externos;
- e-mail;
- scripts;
- CSP;
- MkDocs;
- documentos legais;
- terceiros.

O gate não consulta a internet nem substitui revisão jurídica atualizada.

### Mensal

- spam/abuso da caixa;
- usuários/sessões;
- MFA;
- `/stats`;
- quota;
- eventuais DMARC reports.

### Trimestral

- Aviso de Privacidade;
- Termos;
- comportamento real do site;
- auditoria de rede;
- inventário;
- retenção;
- contratos/políticas do fornecedor;
- fontes normativas oficiais;
- transferências;
- controles de e-mail.

### Anual

- revisão ampla de arquitetura e documentos;
- `security.txt`;
- Confluence;
- plano de resposta a incidentes;
- necessidade de formulário/canal novo.

## Gatilhos imediatos

Revisar sem esperar a data quando houver:
- analytics/pixel/CDN;
- novo formulário;
- conta/login;
- comentários/upload;
- publicidade;
- nova hospedagem;
- novo provedor de e-mail;
- mudança de domínio;
- mudança DMARC para enforcement;
- incidente;
- mudança relevante de lei/regulação;
- atividade comercial organizada.
