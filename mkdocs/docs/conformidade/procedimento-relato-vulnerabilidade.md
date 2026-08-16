# Procedimento interno — relato de vulnerabilidade

> **Motivo do documento:** definir um fluxo consistente quando alguém comunicar possível falha de segurança.
>
> **Fundamento:** prevenção, segurança, responsabilização e coordenação responsável de vulnerabilidades; RFC 9116 como mecanismo de descoberta do canal.
>
> **Regra de manutenção:** revisar quando mudar o canal público, provedor, superfície do site ou processo de resposta a incidentes.

## 1. Recebimento

Ao receber relato:
1. registrar data/hora;
2. atribuir identificador interno;
3. evitar encaminhamento desnecessário do conteúdo;
4. confirmar recebimento quando possível.

## 2. Triagem

Classificar:
- recurso afetado;
- reprodutibilidade;
- impacto potencial;
- exposição de dados pessoais;
- dependência da KingHost/LWSA;
- necessidade de contenção imediata.

## 3. Minimização

Não solicitar ao pesquisador:
- credenciais reais;
- cópia ampla de banco ou log;
- dados pessoais de terceiros;
- exploração adicional quando a evidência já for suficiente.

## 4. Contenção

Se houver risco atual:
- limitar acesso;
- revogar credenciais/sessões quando pertinente;
- corrigir configuração;
- acionar fornecedor;
- preservar evidência mínima.

## 5. Validação e correção

Se a falha estiver no próprio repositório:
- corrigir;
- testar;
- executar validadores;
- revisar impacto de regressão.

Se estiver na KingHost:
- abrir chamado;
- informar somente dados necessários;
- guardar protocolo/evidência em local restrito.

## 6. Dados pessoais

Se o relato revelar incidente com dados pessoais, executar também o procedimento de incidentes previsto na governança de privacidade.

## 7. Retorno ao pesquisador

Quando apropriado, informar confirmação do problema, correção/mitigação e encerramento.

Não divulgar detalhes que aumentem o risco antes da correção.

## 8. Encerramento

Registrar causa, correção, data, testes realizados, documentos atualizados e ação preventiva.

A cópia preenchida do registro é privada.
