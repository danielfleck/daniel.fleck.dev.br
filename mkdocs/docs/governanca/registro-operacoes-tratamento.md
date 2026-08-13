# Registro Simplificado de Operações de Tratamento — daniel.fleck.dev.br

**Responsável:** Daniel Rodrigo Fleck  
**Versão interna:** 3  
**Revisão:** 13/08/2026  
**Escopo:** operações de tratamento relacionadas ao site pessoal `daniel.fleck.dev.br`.

## 1. Objetivo

Manter inventário simplificado das categorias de tratamento relacionadas ao site, sem criar uma base de visitantes. O documento descreve operações, finalidades e responsabilidades em nível de governança.

Não inserir IPs específicos, nomes de visitantes, conteúdo de logs, mensagens individuais ou documentos de identidade, salvo em registro restrito de caso concreto quando necessário e proporcional.

## 2. Operações identificadas

| Operação | Titulares | Dados/categorias | Origem | Finalidade | Papel do responsável | Outros agentes | Retenção/critério |
|---|---|---|---|---|---|---|---|
| Entrega do site e geração de registros técnicos | visitantes | IP, data/hora, requisição, status, bytes, Referer quando recebido, User-Agent e outros dados técnicos | infraestrutura HTTP/HTTPS KingHost | entrega, segurança, operação e diagnóstico | o código não implementa coleta própria; o responsável controla apenas usos que determinar | KingHost/LWSA conforme operação | suporte informou 90 dias para logs brutos HTTP; não extrapolar a outros registros sem confirmação |
| Consulta administrativa a `/stats` ou ferramenta equivalente | visitantes | estatísticas e registros técnicos disponibilizados | painel/serviço de hospedagem | diagnóstico, segurança, suporte e investigação de abuso | controlador da consulta/uso que determinar | KingHost/LWSA | sem exportação rotineira; cópia excepcional somente pelo tempo necessário |
| Comunicação voluntária por e-mail | remetentes | e-mail, nome informado, conteúdo, anexos e metadados | mensagem enviada pelo próprio remetente | responder e dar andamento à comunicação | controlador | provedor de e-mail | conforme finalidade, obrigação aplicável e exercício de direitos |
| Preservação/fornecimento decorrente de requisição válida | titulares relacionados ao escopo solicitado | registros específicos existentes | KingHost e/ou evidência excepcionalmente preservada | cumprimento de obrigação, preservação e exercício regular de direitos | controlador das providências que determinar | KingHost/LWSA e autoridade competente | conforme ordem/requisição e legislação aplicável |
| Registro de incidente de segurança envolvendo dados pessoais | titulares potencialmente afetados | circunstâncias, categorias de dados, volume estimado, risco e providências | investigação do incidente | prestação de contas, segurança e cumprimento regulatório | controlador | provedor/outros agentes quando envolvidos | no mínimo 5 anos para o registro de incidentes, conforme RCIS, salvo prazo superior aplicável |

## 3. O que o código do site não faz atualmente

- não cria conta de usuário;
- não oferece formulário próprio de captação;
- não utiliza analytics próprio ou pixel de marketing;
- não cria cookie próprio de rastreamento/perfilização;
- não mantém banco próprio de visitantes;
- não carrega automaticamente scripts, fontes, imagens ou iframes de terceiros na aplicação principal;
- não realiza perfilização comercial de visitantes.

## 4. Finalidades próprias do provedor

O Contrato de Hospedagem da KingHost contém previsão contratual de usos próprios de dados/registros pelo provedor para melhoria de sistemas e criação/aprimoramento de serviços. Essas finalidades não são determinadas pelo responsável do site e não devem ser registradas como finalidade própria de Daniel.

A qualificação da KingHost/LWSA deve ser feita por operação: pode haver atuação em nome do cliente e também tratamentos em que o provedor determina finalidade própria.

## 5. Bases legais a avaliar por operação

Não utilizar consentimento como fundamento genérico da navegação. As hipóteses devem ser escolhidas por finalidade concreta. Conforme o caso podem ser avaliados:

- legítimo interesse, mediante teste de finalidade, necessidade e balanceamento/salvaguardas;
- cumprimento de obrigação legal ou regulatória;
- exercício regular de direitos;
- procedimentos preliminares relacionados a contrato quando a comunicação do titular tiver essa finalidade.

Legítimo interesse não deve ser aplicado a dados pessoais sensíveis.

## 6. Gatilhos de revisão

Revisar antes de ativar formulário, login, comentários, analytics, publicidade, pixel, cookie não essencial, banco de usuários, upload, CDN/biblioteca externa automática ou integração que altere substancialmente os dados tratados.

Revisar também quando houver alteração material do contrato/política do provedor ou mudança de classificação de risco.

## 7. Evidências e referências

- Política de Privacidade pública V4.
- Termos de Uso públicos V3.
- Git/GitHub.
- due diligence do provedor.
- documentos contratuais e política de privacidade KingHost/LWSA.
- teste de legítimo interesse.
- matriz normativa LGPD/MCI/ANPD.

## 8. Histórico

- V1 — 08/08/2026: criação.
- V2 — 09/08/2026: inclusão de finalidades próprias do provedor e refinamento de papéis por operação.
- V3 — 13/08/2026: sincronização com Privacidade V4/Termos V3, atualização do escopo para site pessoal e referência aos novos documentos de enquadramento e legítimo interesse.
