# Política Simplificada de Segurança e Resposta a Incidentes — daniel.fleck.dev.br

**Versão interna:** 4  
**Revisão:** 13/08/2026

## 1. Princípio

Aplicar controles proporcionais à arquitetura simples do site, priorizando redução de superfície de ataque, minimização de dados, continuidade e rastreabilidade.

## 2. Controles atuais

- HTTPS;
- CSP no HTML para diretivas compatíveis com entrega por `meta`;
- recursos automáticos do site principal servidos pelo próprio domínio;
- `no-referrer`;
- Git/GitHub;
- credenciais individuais;
- MFA quando disponibilizado;
- FTP desativado por padrão;
- acesso administrativo restrito;
- ausência de banco próprio de visitantes;
- ausência de analytics/pixels próprios;
- validações antes do commit;
- separação entre raiz pública e fontes de desenvolvimento.

### Observação sobre `frame-ancestors`

`frame-ancestors` não funciona quando definido em CSP entregue por `<meta>`. A diretiva deve ser removida desse local para não criar falsa impressão de proteção. A proteção anti-framing definitiva deve ser testada e entregue como header HTTP pelo servidor/proxy. O `/docs/` deve ser testado separadamente porque Material for MkDocs utiliza JavaScript inline.

## 3. Credenciais

- senhas fortes e exclusivas;
- gerenciador de senhas recomendado;
- MFA quando disponível;
- não compartilhar segredos;
- revogar acessos temporários;
- não versionar tokens/chaves;
- revisar sessões e integrações administrativas.

## 4. Software e configuração

- usar versões suportadas;
- aplicar correções;
- remover serviços desnecessários;
- revisar CSP ao alterar recursos;
- avaliar dependências externas antes de ativação;
- reconstruir e validar artefatos derivados.

## 5. Continuidade

- código em Git;
- documentação técnica e documentos completos de governança em MkDocs/Git;
- Confluence mantido como camada de resumo, contexto e apontamento para a fonte completa;
- testar restauração a partir de clone limpo;
- não presumir que backup/retenção do provedor substitua cópia própria.

## 6. Monitoramento proporcional

- observar disponibilidade, erros e alertas;
- consultar `/stats`/logs detalhados somente quando necessário;
- não usar para publicidade/perfilização;
- evitar exportação rotineira de dados individualizados;
- documentar exportações excepcionais relevantes;
- revisar MFA e serviços administrativos.

## 7. Fluxo de incidente

1. detectar;
2. registrar data/hora do conhecimento;
3. conter;
4. preservar evidências necessárias;
5. identificar se há dados pessoais afetados;
6. estimar titulares/volume quando possível;
7. avaliar risco/dano;
8. corrigir causa;
9. mitigar efeitos;
10. avaliar comunicação à ANPD e titulares;
11. registrar justificativa da comunicação ou não comunicação;
12. concluir e revisar controles.

## 8. Comunicação e registros

O Regulamento de Comunicação de Incidente de Segurança da ANPD deve ser consultado na versão vigente. Incidentes que possam acarretar risco ou dano relevante exigem avaliação de comunicação. Os registros de incidentes envolvendo dados pessoais devem ser mantidos por pelo menos cinco anos, inclusive os não comunicados, conforme o RCIS.

## 9. Meta interna

Iniciar triagem tão cedo quanto possível, idealmente em até 24 horas do conhecimento, sem usar a meta interna como substituta do prazo regulatório aplicável.

## 10. Histórico

- V1 — 08/08/2026: criação.
- V2 — 08/08/2026: credenciais/MFA/FTP.
- V3 — 09/08/2026: monitoramento proporcional e links externos.
- V4 — 13/08/2026: MkDocs definido como cópia completa e durável da governança, Confluence como resumo/apontamento, correção conceitual de `frame-ancestors`, validação específica de `/docs/` e continuidade documental independente do Confluence.
