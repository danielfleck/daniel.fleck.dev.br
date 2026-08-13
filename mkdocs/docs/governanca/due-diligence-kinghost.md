# Due Diligence da KingHost — Logs, Estatísticas, LGPD, Documentos e Headers

**Data inicial:** 08/08/2026  
**Versão interna:** 4  
**Revisão:** 13/08/2026  
**Classificação:** documento completo de governança no MkDocs; evidências integrais de atendimentos permanecem restritas quando não precisam ser públicas.

## 1. Objetivo

Distinguir fatos confirmados, limitações documentais, pendências e decisões de mitigação relativas à infraestrutura KingHost.

## 2. Logs brutos — atendimento de 08/08/2026

O suporte informou retenção ordinária de **90 dias** para logs brutos HTTP.

O exemplo apresentado continha host, IP de origem, data/hora com fuso, método, recurso, versão HTTP, status, bytes, `Referer` quando existente e `User-Agent`.

O exemplo não evidenciou porta lógica de origem. Isso não comprova ausência do campo em outras camadas.

## 3. Pendências de logs

Permanecem como questões de diligência:
1. guarda da porta lógica quando necessária à identificação inequívoca;
2. camada em que o dado é mantido;
3. canal de preservação;
4. preservação antes do fim da retenção ordinária;
5. distinção entre logs brutos e `/stats`.

## 4. Cabeçalhos HTTP — atendimento de 13/08/2026

O suporte informou, com base na documentação do ambiente Linux:

- disponibilidade de `mod_headers`/`Header always set` via `.htaccess`;
- possibilidade de configurar `Content-Security-Policy`, `X-Frame-Options` e `Referrer-Policy`;
- aplicação a respostas de HTML estático atendidas pelo contexto Apache;
- herança normal de um `.htaccess` da raiz por subdiretórios, salvo regra mais específica;
- ausência de restrição de plano documentada especificamente para CSP.

O suporte também informou que sua documentação:
- confirma existência de Varnish/Magic Cache e menciona Nginx em determinados recursos;
- não descreve de forma exaustiva como todas as camadas tratam CSP, X-Frame-Options e Referrer-Policy;
- não permite garantir precedência absoluta entre header do `.htaccess` e eventual header de intermediário;
- não confirma que esses headers sejam enviados por padrão a todos os domínios.

## 5. Decisão decorrente

O repositório define:
- `site/.htaccess`;
- `mkdocs/.htaccess`;
- `site/docs/.htaccess` gerado pelo build.

Porém a configuração somente é considerada **comprovada em produção** depois de observar a resposta final:

```bash
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/docs/
```

Se houver cache intermediário ativo, limpar o cache antes da validação.

## 6. Contrato e finalidades próprias

A cláusula 14.3 do Contrato de Hospedagem permanece ponto de atenção para finalidades próprias do provedor. Não classificar a KingHost como mera operadora em todas as operações.

## 7. `/stats`

Consultar somente para finalidade técnica, segurança, diagnóstico, suporte ou investigação proporcional. Não utilizar para publicidade/perfilização nem tentar identificar deliberadamente visitantes a partir de IP.

## 8. Evidências restritas

Manter fora da documentação pública:
- transcrição/captura integral dos atendimentos;
- contratos e documentos quando a redistribuição não for necessária;
- evidências com IDs, IPs ou dados individuais;
- futuras respostas sobre preservação e porta lógica.

## 9. Histórico

- V1 — 08/08/2026: criação.
- V2 — 09/08/2026: análise contratual e finalidades próprias do provedor.
- V3 — 13/08/2026: arquitetura multipágina e atualização normativa.
- V4 — 13/08/2026: resposta sobre `mod_headers`, `.htaccess`, HTML estático, camadas intermediárias e regra de validação dos headers em produção.
