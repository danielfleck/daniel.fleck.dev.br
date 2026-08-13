# Governança e conformidade — daniel.fleck.dev.br

**Revisão do conjunto:** 13/08/2026  
**Responsável:** Daniel Rodrigo Fleck  
**Escopo:** governança de privacidade, proteção de dados, Marco Civil da Internet, segurança e decisões documentais relacionadas ao site pessoal `daniel.fleck.dev.br`.

## 1. Papel desta seção

Esta seção do MkDocs mantém os **documentos completos e duráveis de governança** do projeto. Os arquivos Markdown são versionados no Git junto com a documentação do site e constituem a cópia canônica de longo prazo desses documentos.

O Confluence não mantém uma segunda cópia integral. Para cada documento de governança, a página correspondente no Confluence contém:

- um resumo executivo;
- o contexto necessário para navegação e decisão;
- o estado/revisão do documento;
- um link para o documento completo publicado no MkDocs.

Essa opção foi adotada para reduzir duplicação e diminuir o risco de perda documental caso o acesso ao Confluence deixe de estar disponível no futuro.

## 2. Estado público de referência

- Política de Privacidade: **Versão 4 — 10/08/2026 às 00:58 (BRT, UTC-3)**.
- Termos de Uso: **Versão 3 — 10/08/2026 às 00:58 (BRT, UTC-3)**.
- Site: estático multipágina, sem cadastro, login, comentários, formulário próprio de captação, analytics próprio, pixels próprios de marketing ou banco próprio de histórico individual de visitantes.

## 3. Regra documental

A regra conceitual continua sendo:

- **Jira:** trabalho a executar e estado da execução;
- **Confluence:** contexto, estratégia, resumo das decisões e ponto de entrada para a governança;
- **MkDocs:** documentação completa e versionada do produto, da implementação e, por decisão de continuidade, dos documentos completos de governança;
- **Git/GitHub:** código, histórico e fonte versionada do MkDocs.

Para documentos que conceitualmente pertencem ao Confluence, aplica-se a exceção de continuidade: **texto completo no MkDocs; resumo e apontamento no Confluence**.

## 4. Documentos completos preservados aqui

1. [Registro Simplificado de Operações de Tratamento](registro-operacoes-tratamento.md)
2. [Due Diligence da KingHost](due-diligence-kinghost.md)
3. [Procedimento de Titulares, Notificações e Requisições Oficiais](procedimento-titulares-requisicoes.md)
4. [Política Simplificada de Segurança e Resposta a Incidentes](politica-seguranca-incidentes.md)
5. [Controle de Versões — Termos de Uso e Política de Privacidade](controle-versoes-documentos-legais.md)
6. [Matriz de Aplicabilidade dos Documentos da KingHost](matriz-documentos-kinghost.md)
7. [Memória de Enquadramento — Agente de Tratamento de Pequeno Porte](enquadramento-agente-pequeno-porte.md)
8. [Teste de Balanceamento — Legítimo Interesse](teste-legitimo-interesse.md)
9. [Matriz de Aplicabilidade — LGPD, Marco Civil e ANPD](matriz-lgpd-marco-civil-anpd.md)
10. [Decisão — Fronteira Documental Jira × Confluence × MkDocs](decisao-fronteira-documental.md)
11. [Retrospectiva — Migração Vercel → KingHost](retrospectiva-migracao-vercel-kinghost.md)
12. [Retrospectiva — Laboratório PostgreSQL/Supabase](retrospectiva-laboratorio-supabase.md)
13. [Retrospectiva — Roadmap GitHub](retrospectiva-roadmap-github.md)
14. [Template de História de Usuário](template-historia-usuario.md)

## 5. Limite entre documento e evidência

O documento completo pode ser público sem que as **evidências de casos concretos** também sejam publicadas. Não incorporar ao MkDocs:

- IPs ou linhas de log individualizadas;
- documentos de identidade de titulares;
- anexos de incidentes contendo dados pessoais;
- tokens, senhas, chaves SSH, cookies de sessão ou segredos;
- capturas de painel que exponham credenciais ou identificadores desnecessários;
- documentos recebidos de autoridades quando houver sigilo ou restrição.

Quando uma evidência restrita existir, o documento registra sua existência e sua finalidade, mas a evidência deve ser preservada em armazenamento apropriado fora da raiz pública.

## 6. Gatilhos de revisão geral

Revisar o conjunto quando ocorrer mudança material em:

- arquitetura de coleta do site;
- cookies, analytics, publicidade, autenticação, formulários ou uploads;
- provedor de hospedagem;
- contrato ou política de privacidade da KingHost/LWSA;
- tratamento de dados sensíveis ou de grupos vulneráveis;
- escala/frequência do tratamento;
- regras da ANPD aplicáveis;
- mecanismo de logs/preservação;
- canal de atendimento aos titulares;
- ocorrência de incidente relevante.

## 7. Referências principais

- Lei nº 13.709/2018 — LGPD.
- Lei nº 12.965/2014 — Marco Civil da Internet.
- Decreto nº 8.771/2016, com alterações posteriores.
- Resolução CD/ANPD nº 2/2022.
- Resolução CD/ANPD nº 15/2024.
- Resolução CD/ANPD nº 18/2024.
- Guia Orientativo da ANPD sobre Legítimo Interesse.
- Guia de Segurança da Informação para Agentes de Tratamento de Pequeno Porte.
