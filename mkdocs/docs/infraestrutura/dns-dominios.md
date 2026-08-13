# DNS e domínios

O domínio principal é `daniel.fleck.dev.br`. O registro/gestão de domínio ocorre no Registro.br, onde foi configurada a delegação para os servidores DNS da KingHost.

`daniel.fleck.nom.br` funciona como endereço alternativo e foi ajustado para redirecionar ao domínio principal.

## Procedimento para alteração

1. registrar a mudança pretendida em tarefa apropriada;
2. verificar qual camada deve ser alterada: Registro.br, DNS KingHost ou configuração de redirecionamento;
3. aplicar apenas os registros necessários;
4. aguardar propagação quando aplicável;
5. validar resolução DNS;
6. validar HTTPS;
7. validar redirecionamentos e canonical;
8. registrar o estado técnico resultante nesta documentação se houver mudança permanente.

## Cuidados

- não duplicar zonas DNS concorrentes;
- não remover registros sem conhecer sua função;
- evitar publicar valores administrativos que não sejam necessários para explicar a arquitetura;
- após migração de hospedagem, conferir se registros antigos de Vercel ou outros provedores ainda permanecem ativos sem necessidade.
