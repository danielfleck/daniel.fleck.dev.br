# Documentação técnica do daniel.fleck.dev.br

Esta documentação descreve o **produto técnico** `daniel.fleck.dev.br`: arquitetura, desenvolvimento, infraestrutura, operação, segurança e procedimentos de manutenção.

## Fronteira documental

A documentação adota uma separação explícita de responsabilidades:

- **MkDocs:** estado técnico do produto e sua implementação.
- **Jira:** trabalho a realizar, prioridades, bloqueios e andamento.
- **Confluence:** camada de contexto e navegação; para documentos de governança preservados por longo prazo, mantém resumo e link para a versão completa.
- **MkDocs — governança:** mantém também os documentos completos de governança que precisam de conservação durável, versionados no Git.
- **GitHub:** código, histórico de commits e fontes versionadas do MkDocs.

A mesma mudança pode gerar registros nos três sistemas sem duplicar a finalidade. Exemplo: a tarefa de migração fica no Jira; o Confluence mantém o resumo/contexto da decisão; e o MkDocs mantém a configuração técnica resultante e, quando houver requisito de continuidade, o documento completo de governança correspondente.

## Escopo desta documentação

A documentação cobre:

- estrutura estática multipágina;
- diretórios e fontes de verdade;
- criação e manutenção de Blog, Portfólio e Erros e Soluções;
- scripts Python usados apenas em desenvolvimento;
- geração de índices, tags, SEO e sitemap;
- build e publicação do MkDocs;
- hospedagem, DNS e deploy;
- segurança por arquitetura, CSP, credenciais, logs e runbooks;
- documentos completos de governança destinados à preservação durável, sem incorporar evidências restritas de casos concretos quando não houver necessidade de publicação.

!!! note "Fonte e publicação"
    Os arquivos Markdown ficam em `mkdocs/docs/`. O resultado estático do build é gravado em `site/docs/` e publicado em `/docs/`. A saída gerada não deve ser editada manualmente.

!!! warning "Dados e evidências restritas"
    O texto integral dos documentos de governança é preservado no MkDocs. Isso não transforma evidências individualizadas em conteúdo público: não publique tokens, senhas, chaves SSH, cookies de sessão, IPs de visitantes, linhas de log individualizadas, documentos de identidade ou anexos de incidentes sem necessidade e fundamento.
