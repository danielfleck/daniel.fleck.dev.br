# Privacidade por arquitetura

A redução de dados tratados começa na arquitetura.

## Site principal

Não oferece cadastro, autenticação pública, comentários, upload, formulário próprio de captação, publicidade programática, pixel de marketing, analytics comportamental próprio ou banco próprio de histórico individual de visitantes.

Scripts, imagens, fontes e folhas de estilo do site principal são servidos pelo próprio domínio.

## Documentação `/docs/`

A documentação é gerada com Material for MkDocs.

O tema contém suporte a Web Storage (`localStorage` e `sessionStorage`) para estados e preferências funcionais conforme os componentes habilitados. Esses valores são locais ao navegador e não são utilizados pelo responsável para publicidade, analytics ou perfilização.

Na configuração vigente:

- `repo_url` não é utilizado;
- o GitHub é link comum;
- fontes remotas não são configuradas (`font: false`);
- a busca usa índice local;
- `connect-src 'self'` restringe conexões programáticas;
- auditoria headless verifica tentativas de comunicação externa.

## Hospedagem

A ausência de coleta própria não significa ausência de tratamento técnico pela infraestrutura. A KingHost/LWSA pode manter logs e estatísticas conforme o serviço e seus documentos aplicáveis.

## Referência

As qualificações jurídicas, bases legais, direitos, retenções e papéis dos agentes permanecem nos documentos completos de governança e na Política de Privacidade.
