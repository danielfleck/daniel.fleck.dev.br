# Controle de Versões — Termos de Uso e Política de Privacidade

**Revisão interna:** 13/08/2026

## 1. Regra obrigatória

Qualquer alteração textual deve:
1. incrementar a versão do documento alterado;
2. registrar data/hora real e offset;
3. atualizar comentário HTML de controle;
4. acrescentar histórico público;
5. preservar entradas anteriores;
6. registrar motivo/evidência na governança;
7. gerar commit identificável.

As versões são independentes.

## 2. Estado público atual

- **Política de Privacidade: Versão 5 — 13/08/2026 às 18:11 (BRT, UTC-3)**.
- **Termos de Uso: Versão 4 — 13/08/2026 às 18:11 (BRT, UTC-3)**.

## 3. Histórico — Política de Privacidade

### V1 — 08/08/2026 às 22:21
Início do controle formal, estatísticas da hospedagem, retenção informada de logs, segurança, governança de documentos e registro de incidentes.

### V2 — 08/08/2026 às 23:29
Credenciais individuais, MFA quando disponível, controles do provedor e FTP desativado por padrão.

### V3 — 09/08/2026 às 12:59
Finalidades próprias do provedor, referência contratual e refinamento de transparência KingHost/LWSA.

### V4 — 10/08/2026 às 00:58
Refinamento de hospedagem compartilhada, logs, `/stats`, DNS, domínio alternativo e mecanismos de deploy.

### V5 — 13/08/2026 às 18:11
Inclusão explícita de `/docs/` e Material for MkDocs; transparência sobre `localStorage` e `sessionStorage`; remoção de `repo_url`; busca local; CSP própria da documentação; `frame-ancestors` por header HTTP; auditoria headless; e registro da resposta da KingHost sobre `mod_headers`, herança do `.htaccess` e necessidade de verificação prática dos headers finais.

## 4. Histórico — Termos de Uso

### V1 — 08/08/2026 às 22:21
Início do controle formal.

### V2 — 08/08/2026 às 23:29
Medidas administrativas de segurança, MFA e FTP desativado por padrão.

### V3 — 10/08/2026 às 00:58
Refinamento da hospedagem, logs e deploy.

### V4 — 13/08/2026 às 18:11
Inclusão de `/docs/`, Web Storage funcional, busca local, remoção de `repo_url`, CSP/headers específicos, auditoria headless e correção do link direto para a Política de Privacidade.

## 5. Alteração estrutural

Correção de links, canonical, navegação, layout ou diretório sem alteração da redação jurídica não incrementa por si só a versão textual.

## 6. Publicação efetiva

O horário registrado nos documentos deve corresponder à publicação efetiva. Se o webhook/deploy falhar, registrar essa ocorrência e não presumir que o estado do Git já é o estado servido ao visitante.
