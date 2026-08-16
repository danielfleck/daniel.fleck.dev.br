# Governança e conformidade — daniel.fleck.dev.br

**Revisão do conjunto:** 13/08/2026  
**Responsável:** Daniel Rodrigo Fleck  
**Escopo:** privacidade, proteção de dados, Marco Civil, segurança e decisões documentais relacionadas ao site pessoal.

## 1. Papel desta seção

O MkDocs mantém os **documentos completos e duráveis de governança**, versionados em Git.

O Confluence mantém apenas resumo, contexto, status e apontamento para o documento completo. Evidências de caso concreto que contenham dados, identificadores ou informações desnecessárias ao público permanecem em armazenamento restrito.

## 2. Estado público de referência

- Aviso de Privacidade: **Versão 7 — 15/08/2026**.
- Termos de Uso: **Versão 6 — 15/08/2026**.
- Site principal: estático multipágina.
- `/docs/`: Material for MkDocs, com Web Storage funcional documentado.
- `repo_url`: removido; GitHub permanece como link comum.
- comunicação programática de `/docs/`: restringida por `connect-src 'self'`.
- anti-framing: configurado por header HTTP.
- auditoria dinâmica: Chromium headless antes do push.
- direitos do titular: explicitados conforme art. 18 da LGPD.
- notificações/devido processo: ajustados proporcionalmente ao site pessoal, sem conteúdo gerado por visitantes.
- cadeia do serviço de e-mail KingHost/LWSA: localização integral não confirmada; eventual transferência internacional permanece em diligência.

## 3. Regra documental

- **Jira:** trabalho e estado da execução;
- **Confluence:** contexto, resumo e navegação;
- **MkDocs:** documentação técnica e governança completa/durável;
- **Git/GitHub:** código, histórico e fonte versionada.

Arquivos `*-resumo.md` não devem ser mantidos no MkDocs; os resumos pertencem ao Confluence.

## 4. Documentos completos

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
11. [Privacidade e Termos após a inclusão do MkDocs](privacidade-termos-mkdocs-2026-08-13.md)
12. [Retrospectiva — Migração Vercel → KingHost](retrospectiva-migracao-vercel-kinghost.md)
13. [Retrospectiva — Laboratório PostgreSQL/Supabase](retrospectiva-laboratorio-supabase.md)
14. [Retrospectiva — Roadmap GitHub](retrospectiva-roadmap-github.md)
15. [Template de História de Usuário](template-historia-usuario.md)

## 5. Limite entre documento e evidência

Não publicar automaticamente no MkDocs:
- IPs ou linhas individualizadas de log;
- documentos de identidade;
- anexos de incidente com dados pessoais;
- tokens, senhas, chaves, cookies ou segredos;
- capturas administrativas com identificadores desnecessários;
- documentos oficiais restritos ou sigilosos;
- transcrição integral de atendimento que deva permanecer como evidência privada.

## 6. Gatilhos de revisão

Revisar quando houver mudança material em:
- coleta, formulários, contas ou upload;
- cookies ou Web Storage;
- analytics, publicidade ou pixels;
- plugins/tema MkDocs;
- integração automática com terceiros;
- CSP e cabeçalhos HTTP;
- hospedagem, contrato ou política do provedor;
- logs/preservação;
- classificação de risco;
- normas aplicáveis;
- incidente relevante.
