# Logs e estatísticas

O código do site não implementa sistema próprio de logs de visitantes nem ferramenta própria de analytics. A infraestrutura da KingHost produz registros técnicos e disponibiliza determinadas informações por interfaces administrativas.

## Limites técnicos

Em hospedagem compartilhada, o mantenedor não administra diretamente componentes de rede, webserver ou logging de baixo nível. Sua visibilidade é limitada aos registros e interfaces que o serviço coloca sob seu acesso.

## `/stats`

A área de estatísticas é consultada somente quando existe finalidade técnica concreta, como:

- diagnóstico de erro;
- indisponibilidade;
- investigação de abuso;
- suporte;
- análise técnica de comportamento do serviço.

Não utilizar para perfilização, publicidade ou tentativa deliberada de identificar visitantes. Não exportar rotineiramente registros individualizados apenas para criar histórico paralelo.

## Retenção informada pelo provedor

O suporte informou retenção ordinária de 90 dias para logs brutos HTTP. Essa informação é tratada como fato do atendimento e não deve ser extrapolada automaticamente para todos os registros ou para a interface `/stats`.

A documentação técnica não deve reproduzir IPs reais ou linhas individualizadas. Questões de obrigação legal, preservação e papéis dos agentes ficam na governança interna.
