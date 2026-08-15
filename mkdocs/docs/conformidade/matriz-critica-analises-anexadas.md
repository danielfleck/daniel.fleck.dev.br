# Matriz crítica das análises anexadas

> **Motivo do documento:** registrar o que foi aproveitado, corrigido ou rejeitado nas análises externas fornecidas em 14/08/2026.
> **Fundamento:** qualidade da evidência, responsabilização e necessidade de usar norma/fonte primária para afirmações de conformidade.
> **Regra de manutenção:** uma nova análise externa não substitui automaticamente esta matriz; a conclusão deve ser confrontada com norma oficial, contrato e comportamento real.

## Critérios

- **Aceito:** compatível com fonte primária e cenário.
- **Aceito com ressalva:** útil, mas depende do caso ou estava formulado de maneira ampla.
- **Rejeitado:** contradiz evidência mais forte ou norma aplicável.
- **Pendente:** falta informação suficiente.

## Conclusões

| Tema | Tratamento | Razão |
|---|---|---|
| LGPD pode ser relevante mesmo em site pessoal com portfólio profissional | Aceito | não é prudente apoiar toda a governança na exceção de uso exclusivamente particular |
| KingHost é sempre operadora | Rejeitado | papéis variam por operação e existem finalidades próprias do fornecedor |
| webmail do plano está comprovadamente no Brasil | Rejeitado | suporte não confirmou localização; política LWSA admite prestadores no exterior |
| 90 dias é retenção legal de e-mail | Rejeitado | não há prazo geral desse tipo; 90 dias é limite interno escolhido para contato simples encerrado |
| 90 dias de logs HTTP | Aceito como evidência de suporte | informação escrita do suporte, não cláusula/garantia universal |
| não preciso criar coleta própria de IP/porta | Aceito | deveres de registros dependem do papel e não justificam duplicação de logs |
| formulário com CAPTCHA é obrigatório/recomendado de imediato | Rejeitado nesta arquitetura | criaria coleta, endpoint e terceiro automático; e-mail dedicado é mais simples no cenário atual |
| aviso antes do e-mail | Aceito como melhoria de transparência | não é consentimento; alerta sobre dados sensíveis e papel do provedor |
| SPF/DKIM/DMARC são medidas úteis | Aceito | autenticação de domínio e segurança de e-mail |
| SPF com `~all` | Rejeitado para o estado atual | suporte/documentação confirmam `-all` para envio exclusivo KingHost |
| DKIM exclusivo do cliente | Rejeitado como padrão KingHost atual | documentação descreve assinatura compartilhada `dkim.kinghost.net` |
| DMARC deve ir direto a `reject` | Rejeitado | primeiro observar autenticação e relatórios agregados |
| `ruf` deve ser configurado para ter mais visibilidade | Rejeitado nesta etapa | failure reports aumentam risco de PII e volume |
| inventário integral deve ser público | Rejeitado | registro simplificado é governança; evidência individual não deve ser publicada por padrão |
| ANPD precisa ser mencionada | Aceito | V7 mantém explicitamente o canal/direito de petição |
| revisão periódica | Aceito | implementada com gate por commit, calendário e revisão trimestral |
