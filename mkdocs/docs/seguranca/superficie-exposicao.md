# Superfície de exposição

A arquitetura busca manter acessível pela web apenas o que precisa ser público.

## Conteúdo público

- páginas HTML do site;
- CSS/JS próprios;
- imagens publicáveis;
- sitemap e robots;
- documentação MkDocs gerada.

## Conteúdo que não deve ser web-publicado

- fontes Python;
- testes;
- `.venv`;
- templates como arquivos navegáveis se não houver motivo;
- backups privados;
- governança completa e evidências restritas;
- `.git`;
- arquivos de credenciais;
- artefatos locais `dist/`;
- metadados `*.egg-info/`.

## Serviços administrativos

FTP é desativado por padrão. Acesso administrativo interativo deve ser usado apenas quando necessário. O canal gerenciado de deploy não deve ser confundido com exposição irrestrita de SSH ao uso cotidiano.

## Recursos externos

A introdução de CDN, biblioteca, iframe, fonte ou script externo altera a superfície de exposição e deve ser analisada antes de entrar no site. Isso também pode exigir revisão de CSP e de documentação de privacidade.
