# Credenciais e acessos

## Princípios

- senha forte e exclusiva por serviço;
- autenticação multifator quando disponível;
- menor privilégio;
- nenhum segredo no Git;
- acesso temporário revogado ao fim da atividade;
- serviços administrativos desativados quando desnecessários.

## Serviços

### GitHub

Conta individual e MFA. Chaves/tokens devem ter escopo mínimo e nunca aparecer na documentação.

### Hospedagem

Painel protegido por credenciais próprias e MFA quando disponibilizado. Recursos administrativos do plano devem permanecer restritos.

### E-mail

Conta usada como canal público, mas autenticação e mensagens não fazem parte da aplicação web.

### FTP

Desativado por padrão. Se uma manutenção exigir FTP, habilitar pelo menor tempo possível e desativar ao terminar.

### SSH

Distinguir acesso interativo administrativo de mecanismos técnicos utilizados pela publicação gerenciada. Não registrar usuário, porta personalizada ou chave privada.

## Incidente de credencial

Ao suspeitar de comprometimento: revogar sessões/tokens, alterar credencial, revisar logs administrativos disponíveis, verificar mudanças não autorizadas e documentar o incidente conforme o runbook.
