# Retrospectiva — Migração Vercel → KingHost

## Contexto

A migração de hospedagem representou uma etapa de consolidação do site pessoal e da disciplina de operação: GitHub como fonte do código, DNS administrado de forma explícita, deploy integrado ao provedor e controles administrativos reduzidos ao necessário.

## Decisões relevantes

- manter o repositório Git como fonte do conteúdo;
- utilizar publicação gerenciada pela hospedagem em vez de manutenção manual cotidiana;
- diferenciar acesso SSH administrativo inicial do canal técnico de deploy;
- manter FTP desativado por padrão;
- separar a frente técnica da frente de governança jurídica/privacidade.

## Evolução documental

A descrição técnica vigente da hospedagem, DNS e deploy passou a pertencer ao MkDocs. Esta retrospectiva conserva o contexto e as razões de governança, sem duplicar o procedimento operacional.

## Referências técnicas

Consultar no MkDocs:

- Infraestrutura → Hospedagem KingHost;
- Infraestrutura → DNS e domínios;
- Infraestrutura → GitHub e deploy;
- Operação → Troubleshooting de webhook.


## Preservação documental

Este texto completo é preservado no MkDocs/Git. A página correspondente no Confluence deve conter apenas um resumo contextual e um link para esta versão completa.
