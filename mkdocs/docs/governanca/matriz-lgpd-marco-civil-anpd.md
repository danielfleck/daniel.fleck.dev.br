# Matriz de Aplicabilidade — LGPD, Marco Civil e ANPD

**Versão:** 1  
**Data:** 13/08/2026

## 1. Objetivo

Registrar as principais normas e orientações consideradas na governança do site e evitar conclusões genéricas sem análise do fato concreto.

| Fonte | Natureza | Relevância para o site | Aplicação/observação |
|---|---|---|---|
| Lei nº 13.709/2018 — LGPD | lei | central | princípios, bases legais, direitos, segurança, agentes, incidentes e prestação de contas |
| Lei nº 12.965/2014 — Marco Civil | lei | relevante | privacidade, registros de conexão/aplicação, preservação e fornecimento conforme enquadramento |
| Decreto nº 8.771/2016 | regulamento MCI | relevante | segurança/guarda e regulamentação do Marco Civil |
| Decreto nº 12.975/2026 | alteração regulamentar | relevante | incluiu art. 15-A sobre porta lógica de origem quando necessária à identificação inequívoca e dever autônomo por provedor sujeito à guarda |
| Resolução CD/ANPD nº 2/2022 | regulamento | relevante | tratamento diferenciado para agentes de pequeno porte; registro simplificado; encarregado; segurança; prazos |
| Resolução CD/ANPD nº 15/2024 | regulamento | relevante | comunicação e registro de incidentes de segurança envolvendo dados pessoais |
| Resolução CD/ANPD nº 18/2024 | regulamento | relevante | atuação do encarregado; deve ser lida em conjunto com a dispensa prevista para pequeno porte quando aplicável |
| Guia ANPD de Legítimo Interesse | orientação | relevante | teste de finalidade, necessidade, balanceamento e salvaguardas |
| Guia de Segurança para agentes de pequeno porte | orientação | relevante | medidas administrativas/técnicas proporcionais |

## 2. Marco Civil — cuidado com a guarda de registros

O art. 15 do Marco Civil estabelece no caput obrigação de guarda por seis meses para provedor de aplicações constituído como pessoa jurídica que exerça a atividade de forma organizada, profissionalmente e com fins econômicos. O próprio artigo contém mecanismos de preservação aplicáveis além do caput.

Portanto, não adotar frases simplificadoras como:

- “todo site precisa manter seis meses de logs”; ou
- “se o responsável não possui materialmente o log, nunca existe obrigação”.

O enquadramento depende do agente, operação, tipo de registro e caso concreto.

## 3. Porta lógica de origem

O art. 15-A do Decreto nº 8.771/2016, incluído pelo Decreto nº 12.975/2026, prevê que o dever de guarda de endereço IP aplicável aos provedores abrange a porta lógica de origem associada quando necessária à identificação inequívoca. A regra é autônoma para cada provedor sujeito ao dever.

A amostra de log recebida da KingHost não evidenciou esse campo. Isso não prova ausência na infraestrutura e justifica manter a pendência formal com o provedor.

## 4. Pequeno porte

A Resolução nº 2/2022 não elimina a LGPD. Flexibilizações dependem do enquadramento e podem ser afastadas em tratamento de alto risco ou por outras condições da norma.

## 5. Incidentes

A Resolução nº 15/2024 deve ser consultada em incidentes que envolvam dados pessoais. O registro de incidentes deve ser mantido por pelo menos cinco anos.

## 6. Atualização

Revisar a matriz quando houver alteração normativa material, nova orientação oficial ou mudança técnica do site que aumente tratamento/risco.

## 7. Referências oficiais

- LGPD: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- Marco Civil: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm
- Decreto nº 8.771/2016: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/decreto/d8771.htm
- Regulamentações ANPD: https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd
