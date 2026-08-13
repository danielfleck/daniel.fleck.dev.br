# Retrospectiva — Laboratório PostgreSQL/Supabase com migrations

## Contexto

O exercício foi criado para transformar alterações estruturais de banco em artefatos SQL versionados, reduzindo dependência de mudanças manuais sem rastreabilidade.

## Aprendizados principais

- iniciar o controle de versão antes das mudanças de schema;
- distinguir conexão PostgreSQL de URL HTTP;
- entender quando `db pull` faz sentido em relação ao estado remoto;
- manter migrations como histórico executável do schema;
- validar mudanças por mais de um mecanismo;
- separar histórico Git do histórico de migrations aplicado pelo Supabase.

## Decisão documental atual

O procedimento técnico do laboratório **não pertence ao MkDocs do `daniel.fleck.dev.br`**, pois descreve outro produto/repositório. Ele deve ser mantido na documentação do próprio repositório `transicao-database-supabase`.

O Confluence preserva apenas esta retrospectiva e decisões/aprendizados do projeto de transição.


## Preservação documental

Este texto completo é preservado no MkDocs/Git. A página correspondente no Confluence deve conter apenas um resumo contextual e um link para esta versão completa.
