# Hospedagem KingHost

O site é hospedado em ambiente compartilhado da KingHost/LWSA. O conteúdo publicado é estático e tem como raiz lógica o diretório `site/` do repositório.

## Limites de administração

O mantenedor administra o conteúdo e os recursos disponibilizados no plano, mas não administra diretamente o webserver subjacente, equipamentos de rede nem sistemas de logging de baixo nível da provedora.

Essa distinção é relevante para operação e troubleshooting: determinadas informações técnicas só existem nas interfaces e registros que o provedor disponibiliza.

## Publicação

A publicação cotidiana utiliza a integração Git gerenciada pela hospedagem. A preparação inicial do diretório remoto exigiu acesso administrativo interativo por SSH, mas esse acesso não é o fluxo normal de deploy.

FTP permanece desativado por padrão e só deve ser habilitado temporariamente para uma atividade administrativa específica, com desativação imediata ao término.

## O que não documentar publicamente

- usuário SSH/FTP;
- chaves;
- senhas;
- token de webhook;
- IDs administrativos desnecessários;
- IPs internos;
- caminhos privados que aumentem a exposição sem benefício documental.

## Continuidade

O GitHub é a fonte de código e histórico. Backups do provedor não substituem a capacidade de reconstruir o site a partir do repositório e das fontes documentais.
