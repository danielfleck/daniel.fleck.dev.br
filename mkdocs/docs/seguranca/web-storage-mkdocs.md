# Web Storage no Material for MkDocs

## Escopo

A área `/docs/` utiliza Material for MkDocs. O JavaScript do tema contém funções de suporte a Web Storage, incluindo `localStorage` e `sessionStorage`.

Web Storage é um mecanismo do navegador para pares chave/valor associados à origem. Ele não é um cookie HTTP e seus valores não são anexados automaticamente às requisições de rede.

## Usos suportados pelo tema

Dependendo das funcionalidades habilitadas, Material for MkDocs pode usar armazenamento local para:

- paleta de cores;
- vínculo/persistência de abas de conteúdo;
- dispensa de avisos;
- escolhas do componente de consentimento;
- estados temporários de integrações, inclusive informações de repositório em `sessionStorage` quando a integração correspondente existe;
- estados de versão/avisos em configurações que habilitem esses recursos.

## Configuração deste site

Nesta versão:

- a paleta é fixa;
- `content.tabs.link` não está habilitado;
- não existe componente de consentimento configurado;
- não existe analytics;
- `repo_url` foi removido;
- o GitHub é apenas link normal;
- `connect-src 'self'` restringe conexões programáticas da documentação;
- a auditoria headless falha se surgir host externo não autorizado.

Assim, a presença do código de suporte do tema não deve ser interpretada como uso de todas as possibilidades de armazenamento em cada visita.

## Compartilhamento

O projeto não contém mecanismo destinado a enviar deliberadamente a terceiros os valores armazenados em `localStorage` ou `sessionStorage`.

Isso é diferente de afirmar que nenhuma informação técnica jamais é tratada: a infraestrutura de hospedagem continua podendo gerar logs HTTP e dados técnicos conforme documentado na Política de Privacidade.

## Revisão

A ativação futura de analytics, `repo_url`, consentimento, plugins, scripts adicionais ou recursos que persistam novas preferências exige:

1. revisão desta página;
2. execução do build;
3. validação estática;
4. auditoria de rede;
5. revisão da Política de Privacidade e, quando pertinente, dos Termos.
