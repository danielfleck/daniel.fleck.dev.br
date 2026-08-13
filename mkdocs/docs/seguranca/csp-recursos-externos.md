# CSP e recursos externos

A Content Security Policy do site principal busca permitir apenas os recursos necessários à aplicação estática.

## Diretivas em `meta`

Diretivas compatíveis com entrega via `<meta http-equiv="Content-Security-Policy">` continuam úteis para restringir scripts, estilos, imagens, fontes, conexões, objetos e formulários conforme a política definida.

`frame-ancestors`, contudo, precisa ser entregue em **header HTTP** e não deve ser mantido no `meta` como se estivesse ativo.

## Proteção anti-framing

A tarefa de segurança deve testar no ambiente KingHost uma solução por header HTTP. O estado só deve ser documentado como “implementado” depois de verificar a resposta real do servidor.

## MkDocs

O Material for MkDocs usa JavaScript inline. Por isso, a política do site principal não deve ser copiada mecanicamente para `/docs/`. Uma política muito restritiva pode quebrar busca, navegação e outros recursos.

## Novos terceiros

Antes de adicionar recurso externo automático:

1. identificar fornecedor e finalidade;
2. confirmar necessidade;
3. avaliar impacto de privacidade e segurança;
4. atualizar CSP;
5. verificar se a Política de Privacidade precisa mudar;
6. testar comportamento sem relaxar diretivas além do necessário.

Links `<a>` comuns para sites externos não são equivalentes a carregar automaticamente scripts, imagens ou iframes desses sites.
