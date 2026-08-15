# Fornecedores, papéis e transferências

> **Motivo do documento:** Manter visão dos agentes, papéis, dependências e pendências de localização/transferência.
> **Fundamento:** LGPD arts. 9, 18 VII, 33-36, 37, 39 e 46; Resolução CD/ANPD nº 19/2024.
> **Regra de manutenção:** cada alteração relevante deve atualizar o motivo/fundamento correspondente e, quando afetar texto público, o racional da seção legal no mesmo commit.


## KingHost/LWSA — hospedagem web

**Papel:** depende da operação.  
**Dados possíveis:** logs técnicos, IP, navegação, estatísticas, dados contratuais.  
**Acesso do responsável:** painel e estatísticas oferecidas; não há controle sobre toda a camada bruta.  
**Evidência:** contrato, política pública, documentação e suporte.

## KingHost/LWSA — e-mail

**Papel:** pode executar tratamento em nome do cliente e possuir finalidades próprias.  
**Dados:** conteúdo, caixas postais, metadados e registros técnicos conforme serviço.  
**Localização:** não fechada para o plano específico. O suporte não confirmou país/cidade.  
**Transferência internacional:** não declarar inexistência. A política LWSA admite transferência de alguns dados a prestadores no exterior.

## Registro/DNS

A zona DNS é gerenciada pela KingHost no cenário documentado. Registros SPF/DMARC são públicos por natureza.

## GitHub

O repositório é público. Não colocar:
- e-mails reais de terceiros;
- relatórios DMARC recebidos;
- `.eml`;
- evidências de incidente;
- credenciais;
- logs individualizados.

## Confluence/Jira

Utilizar para decisão e gestão do projeto, mas não copiar dados pessoais só para documentar. Registrar número de caso interno e resumo anonimizado quando suficiente.

## Avaliação trimestral de fornecedor

Verificar:
- contrato vigente;
- política de privacidade;
- localização/processamento;
- subcontratados quando informados;
- backups;
- retenção;
- incidentes/avisos relevantes;
- MFA/controles disponíveis;
- autenticação de e-mail;
- canais de suporte.
