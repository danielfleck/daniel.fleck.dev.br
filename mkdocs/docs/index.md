# Documentação técnica do daniel.fleck.dev.br

Esta documentação descreve o **produto técnico** `daniel.fleck.dev.br`: sua arquitetura, desenvolvimento, infraestrutura, operação e controles técnicos de segurança.

## Fronteira documental

A regra adotada para o projeto é:

- **MkDocs:** descreve o produto e sua implementação técnica.
- **Jira:** registra trabalho a executar.
- **Confluence:** registra contexto, raciocínio, decisões e planejamento do projeto de transição.
- **GitHub:** mantém código, histórico e documentação técnica versionada.

## Estrutura

A documentação está organizada em:

- [Arquitetura](arquitetura/): estrutura e decisões técnicas vigentes.
- [Desenvolvimento](desenvolvimento/): ambiente local, scripts, testes e criação de conteúdo.
- [Infraestrutura](infraestrutura/): hospedagem, DNS, Git e publicação.
- [Operação](operacao/): build, validação, deploy, rollback e troubleshooting.
- [Segurança](seguranca/): controles técnicos, privacidade por arquitetura e exposição de recursos.

!!! note "Fonte e publicação"
    Os arquivos Markdown ficam em `mkdocs/docs/`. O resultado estático do build é gravado em `site/docs/` e publicado em `/docs/`.
