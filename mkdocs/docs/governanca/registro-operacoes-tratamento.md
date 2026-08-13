# Registro Simplificado de Operações de Tratamento — daniel.fleck.dev.br

**Responsável:** Daniel Rodrigo Fleck  
**Versão interna:** 4  
**Revisão:** 13/08/2026

## 1. Objetivo

Manter inventário simplificado das operações relacionadas ao site sem criar uma base de visitantes.

Não inserir IPs específicos, nomes de visitantes, linhas individualizadas de log ou documentos de identidade neste documento.

## 2. Operações identificadas

| Operação | Titulares | Dados/categorias | Origem | Finalidade | Papel do responsável | Outros agentes | Retenção/critério |
|---|---|---|---|---|---|---|---|
| Entrega do site e registros técnicos | visitantes | IP, data/hora, requisição, status, bytes, Referer quando recebido, User-Agent e outros dados técnicos | infraestrutura KingHost | entrega, segurança, operação e diagnóstico | controla somente os usos que determinar; o código não implementa coleta própria | KingHost/LWSA conforme a operação | suporte informou 90 dias para logs brutos HTTP; não extrapolar para outros registros |
| Consulta administrativa a `/stats` | visitantes | estatísticas e registros disponibilizados | painel de hospedagem | diagnóstico, segurança, suporte e investigação de abuso | controlador da consulta/uso que determinar | KingHost/LWSA | sem exportação rotineira; cópia excepcional pelo tempo necessário |
| Web Storage funcional em `/docs/` | visitantes da documentação | pares chave/valor funcionais do tema no navegador, conforme recursos/interações habilitados | navegador do visitante / Material for MkDocs | estado e preferências da interface e caches temporários quando aplicável | responsável pela configuração publicada; não utiliza para publicidade, analytics ou perfilização | nenhum terceiro é destinatário deliberado desses valores na configuração atual | `localStorage`: conforme navegador/limpeza/substituição; `sessionStorage`: sessão correspondente |
| Comunicação voluntária por e-mail | remetentes | e-mail, nome informado, conteúdo, anexos e metadados | mensagem do remetente | responder e tratar a comunicação | controlador | provedor de e-mail | conforme finalidade, obrigação e exercício de direitos |
| Preservação/fornecimento por requisição válida | titulares relacionados | registros específicos existentes | KingHost e/ou evidência excepcional | obrigação, preservação e exercício de direitos | controlador das providências que determinar | KingHost/LWSA e autoridade competente | conforme ordem/requisição e legislação |
| Registro de incidente com dados pessoais | titulares potencialmente afetados | circunstâncias, categorias, volume, risco e providências | investigação | prestação de contas e cumprimento regulatório | controlador | provedor/outros agentes quando envolvidos | mínimo de 5 anos para o registro do incidente, salvo prazo superior aplicável |

## 3. O que o site não faz

- não cria conta de usuário;
- não oferece formulário próprio de captação;
- não utiliza analytics próprio ou pixel de marketing;
- não cria cookie próprio de rastreamento/perfilização;
- não mantém banco próprio de visitantes;
- não utiliza os valores de Web Storage para publicidade ou perfilização;
- não configura carregamento automático de recursos de terceiros;
- não realiza perfilização comercial.

## 4. Material for MkDocs

A presença de código do tema capaz de usar `localStorage`/`sessionStorage` não significa que todos os recursos possíveis gravem dados em toda visita. O uso depende da configuração e da interação.

A configuração atual mantém:
- paleta fixa;
- `font: false`;
- sem analytics;
- sem `repo_url`;
- GitHub como link comum;
- busca local;
- `connect-src 'self'`.

## 5. Finalidades próprias do provedor

Finalidades definidas pela KingHost/LWSA não devem ser registradas como finalidades próprias do responsável. O papel jurídico deve ser analisado por operação.

## 6. Bases legais

Não utilizar consentimento como fundamento genérico da navegação. Avaliar a base conforme a finalidade concreta. Legítimo interesse não se aplica a dados pessoais sensíveis.

## 7. Gatilhos de revisão

Revisar antes de ativar:
- formulário, login, comentários ou upload;
- analytics, publicidade, pixel ou cookie não essencial;
- novo uso persistente de Web Storage;
- `repo_url`, CDN ou recurso externo automático;
- plugin/tema MkDocs com nova comunicação;
- banco de usuários.

## 8. Evidências e referências

- Política de Privacidade pública **V5**.
- Termos de Uso públicos **V4**.
- Git/GitHub.
- Due diligence da KingHost.
- documentos contratuais/política do provedor.
- teste de legítimo interesse.
- matriz LGPD/MCI/ANPD.

## 9. Histórico

- V1 — 08/08/2026: criação.
- V2 — 09/08/2026: finalidades próprias do provedor e papéis por operação.
- V3 — 13/08/2026: sincronização com a arquitetura multipágina e atualização normativa.
- V4 — 13/08/2026: inclusão de `/docs/`, Web Storage funcional, controles de conexão do MkDocs e referências públicas V5/V4.
