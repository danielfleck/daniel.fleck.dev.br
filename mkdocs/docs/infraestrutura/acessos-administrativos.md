# Acessos administrativos

O princípio aplicado é o menor acesso necessário para manutenção do site.

## Contas principais

Os serviços administrativos relevantes incluem:

- GitHub;
- painel de hospedagem;
- e-mail de contato/administrativo;
- acesso temporário FTP quando necessário;
- acesso administrativo interativo por SSH quando uma tarefa específica exigir.

Cada serviço deve usar credencial individual e autenticação multifator quando disponibilizada.

## Regras

- não reutilizar senhas;
- preferir gerenciador de senhas;
- não versionar `.env`, tokens, chaves ou senhas;
- não enviar segredos a chats, issues ou documentação;
- revogar acesso temporário de terceiros ao fim da atividade;
- manter FTP desativado quando não estiver em uso;
- revisar periodicamente MFA e sessões ativas;
- registrar somente o procedimento, nunca o segredo.

## `/stats`

O acesso à área de estatísticas da hospedagem é administrativo e deve permanecer protegido pelo mecanismo de autenticação disponibilizado pelo provedor. A rota pode existir publicamente enquanto o conteúdo fica protegido por credenciais.
