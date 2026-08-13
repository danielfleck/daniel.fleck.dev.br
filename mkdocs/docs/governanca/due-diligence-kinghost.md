# Due Diligence da KingHost — Logs, Estatísticas, LGPD e Documentos

**Data inicial:** 08/08/2026  
**Versão interna:** 3  
**Revisão:** 13/08/2026  
**Classificação:** documento completo de governança preservado no MkDocs; evidências de casos concretos permanecem fora da raiz pública quando contiverem dados ou identificadores que não precisem ser publicados.

## 1. Objetivo

Documentar informações confirmadas pelo provedor, distinguir fatos de hipóteses, identificar pendências e manter evidência de diligência sobre a infraestrutura usada por `daniel.fleck.dev.br`.

## 2. Fatos confirmados pelo atendimento humano

Em atendimento de 08/08/2026, após pergunta específica sobre logs brutos de acesso HTTP, o suporte informou retenção ordinária de **90 dias**.

O exemplo técnico apresentado continha, entre outros elementos:

- domínio/host;
- IP de origem;
- data e hora com fuso;
- método HTTP;
- recurso solicitado;
- versão HTTP;
- status;
- bytes;
- `Referer` quando existente;
- `User-Agent`.

O exemplo **não evidenciou a porta lógica de origem**. Isso não permite concluir que a porta inexista em outra camada.

## 3. Pendências formais

Solicitar/arquivar resposta do provedor sobre:

1. guarda da porta lógica de origem quando necessária à identificação inequívoca;
2. camada em que esse dado é mantido, quando aplicável;
3. canal formal para requisição cautelar/ordem de preservação;
4. mecanismo de preservação antes do término dos 90 dias;
5. prazo possível de preservação além da retenção ordinária;
6. distinção entre logs brutos e histórico exibido em `/stats`.

A atualização do Decreto nº 8.771/2016 pelo Decreto nº 12.975/2026 tornou essa pendência particularmente relevante: quando houver dever de guarda de endereço IP aplicável ao provedor, a regulamentação passou a abranger a porta lógica de origem quando necessária à identificação inequívoca, de forma autônoma para cada provedor sujeito ao dever.

## 4. Contrato e finalidades próprias do provedor

A cláusula 14.3 do Contrato de Hospedagem foi registrada como ponto de atenção porque prevê uso de dados/registros da base do provedor para atividades próprias de melhoria e criação de serviços.

Consequências de governança:

- não classificar a KingHost como mera operadora em todas as operações;
- não atribuir a Daniel finalidades determinadas exclusivamente pelo provedor;
- acompanhar Política de Privacidade e Contrato de Hospedagem;
- revisar a Política pública somente quando mudança material afetar transparência necessária.

## 5. `/stats`

Princípios:

- consultar apenas por finalidade técnica, segurança, diagnóstico, suporte ou investigação;
- não usar para publicidade/perfilização;
- não tentar identificar deliberadamente pessoas a partir de IP;
- não exportar rotineiramente apenas para criar histórico;
- proteger acesso administrativo;
- documentar exportações excepcionais necessárias.

## 6. Não criar coleta adicional por precaução

A retenção limitada do provedor não justifica instalar analytics, pixels ou banco próprio de visitantes. Nova coleta exige finalidade real, base legal, retenção, medidas de segurança e revisão prévia do registro e da Política de Privacidade quando material.

## 7. Controle de documentos do provedor

Ao receber nova versão contratual/política:

1. salvar cópia;
2. registrar data de consulta/aceite quando houver;
3. comparar com versão anterior;
4. avaliar dados, finalidades, papéis, retenção, suboperadores, segurança, transferências e incidentes;
5. atualizar governança;
6. atualizar documento público somente se houver impacto material.

## 8. Evidências complementares a manter fora da documentação pública

- exportação/captura do atendimento;
- contrato vigente;
- política de privacidade vigente;
- documentos aplicáveis ao plano;
- futuras respostas sobre porta lógica e preservação.

## 9. Histórico

- V1 — 08/08/2026: criação.
- V2 — 09/08/2026: análise contratual e finalidades próprias do provedor.
- V3 — 13/08/2026: sincronização com arquitetura multipágina, atualização normativa sobre porta lógica e reforço da separação entre evidência privada e resumo público.
