# GitHub e deploy

O código-fonte é mantido no GitHub. A publicação utiliza o mecanismo gerenciado de integração Git disponibilizado pela KingHost.

## Fluxo normal

```text
edição local
   ↓
rebuild + build docs + validação
   ↓
git diff
   ↓
commit
   ↓
push para GitHub
   ↓
integração/webhook da hospedagem
   ↓
publicação
   ↓
verificação pós-deploy
```

## SSH

A configuração inicial utilizou acesso administrativo interativo por SSH para preparar o diretório e realizar a primeira configuração. Esse acesso não deve ser confundido com o canal técnico utilizado internamente pela integração gerenciada de deploy.

A documentação não deve afirmar genericamente que “SSH está desativado” se o mecanismo gerenciado depende de recursos SSH. A descrição correta distingue acesso administrativo interativo do canal técnico de publicação.

## FTP

FTP é exceção operacional: permanece desativado por padrão e é habilitado apenas quando uma tarefa específica exigir.

## Webhook

Falhas de entrega do webhook devem ser diagnosticadas pelo histórico de deliveries do GitHub. Uma tentativa que retorna `failed to connect to host` prova falha de conexão naquela entrega, não identifica por si só a causa raiz.

## Segurança

Nunca registre na documentação pública credenciais, chaves, tokens, IDs de webhook ou URLs administrativas contendo identificadores desnecessários.
