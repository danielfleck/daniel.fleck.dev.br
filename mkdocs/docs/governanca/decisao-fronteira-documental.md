# Decisão — Fronteira Documental Jira × Confluence × MkDocs

**Data da decisão:** 13/08/2026  
**Status:** adotada e refinada pela decisão de continuidade documental.

## 1. Contexto

O projeto de transição profissional e o site acumularam registros em GitHub, Confluence, Jira, páginas públicas e arquivos locais. O crescimento do conteúdo exigiu separar três naturezas diferentes de informação: trabalho, contexto/decisão e estado técnico do produto.

Também foi considerado um requisito de continuidade: parte da governança precisa permanecer disponível por vários anos, e uma plataforma SaaS não deve ser o único local em que o texto completo esteja preservado.

## 2. Regra conceitual

> **Se descreve o produto ou sua implementação → MkDocs.**  
> **Se descreve trabalho → Jira.**  
> **Se descreve contexto, estratégia, raciocínio ou decisão → Confluence.**

Essa regra continua determinando **onde a informação é classificada**.

## 3. Exceção de continuidade para documentos do Confluence

Para documentos que conceitualmente pertencem ao Confluence, mas precisam de preservação durável, aplica-se a seguinte regra operacional:

> **MkDocs mantém o documento completo em Markdown, versionado no Git.**  
> **Confluence mantém um resumo, o contexto da página e um link para o documento completo no MkDocs.**

Consequências:

- não há duas cópias integrais que precisem ser atualizadas manualmente;
- o texto completo sobrevive independentemente do Confluence;
- o histórico Git fornece rastreabilidade das alterações do documento;
- o Confluence continua sendo a camada de navegação contextual e decisão;
- evidências restritas de casos concretos não são publicadas apenas porque o documento-base está no MkDocs.

## 4. Jira

É a fonte do **trabalho**:

- tarefas e épicos;
- prioridades;
- bloqueios;
- critérios de aceitação;
- estado de execução;
- estudos, correções e entregas ainda pendentes.

Exemplos:

- migrar hospedagem;
- implementar script de build;
- revisar currículo;
- publicar artigo;
- corrigir cabeçalho mobile;
- obter resposta da KingHost sobre porta lógica.

## 5. Confluence

É a camada de **contexto e decisão**. Para cada documento abrangido pela política de continuidade, a página deve conter:

- objetivo/resumo;
- decisão ou conclusão principal;
- estado da revisão;
- relação com o projeto de transição;
- link direto para o texto completo no MkDocs.

O Confluence não deve reproduzir integralmente o conteúdo que já é canônico no MkDocs.

## 6. MkDocs

É a fonte versionada e durável de:

### Produto e implementação

- arquitetura do site;
- estrutura de diretórios;
- scripts e build;
- deploy e DNS;
- segurança técnica;
- troubleshooting;
- manutenção e restauração.

### Governança preservada

- registro de operações de tratamento;
- due diligence de provedor;
- procedimentos de titulares e requisições;
- política de segurança/incidentes;
- controle de versões legais;
- matrizes de aplicabilidade;
- análise de pequeno porte;
- teste de legítimo interesse;
- decisões documentais e retrospectivas que precisem de conservação.

## 7. Git/GitHub

Mantém:

- código;
- commits;
- histórico;
- arquivos Markdown do MkDocs;
- revisão e restauração das versões documentais.

## 8. Exemplo KingHost

- **Jira:** “Migrar hospedagem para KingHost”.
- **Confluence:** resumo da decisão “KingHost foi escolhida por...” + link para o registro durável pertinente.
- **MkDocs:** configuração técnica resultante e, na seção de governança, documento completo de due diligence quando aplicável.

## 9. Roadmap anterior

O Roadmap GitHub e a página pública `/roadmap/` deixam de ser fontes do trabalho corrente. Podem ser mantidos como registro histórico, deixando explícito que o Jira é a fonte atual do trabalho.

## 10. Evidências restritas

A decisão de preservar documentos completos no MkDocs não obriga a publicar evidências individualizadas. Permanecem fora da raiz pública, quando aplicável:

- IPs e logs de pessoas;
- anexos de incidentes;
- credenciais e segredos;
- documentos de identidade;
- requisições oficiais sigilosas;
- capturas administrativas que exponham informação desnecessária.

## 11. Regra de manutenção

Quando um documento de governança for alterado:

1. editar primeiro o Markdown canônico em `mkdocs/docs/governanca/`;
2. revisar a alteração no Git;
3. executar o build/validações do MkDocs;
4. publicar;
5. atualizar a página-resumo do Confluence apenas se o resumo, status, conclusão ou URL precisar mudar.
