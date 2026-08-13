# Verificação pós-deploy

Depois de uma publicação relevante, faça uma verificação curta e objetiva.

## Checklist

1. abrir a home por HTTPS;
2. confirmar que o commit esperado chegou ao ambiente;
3. abrir a página alterada;
4. testar navegação principal;
5. testar `/blog/`, `/portfolio/`, `/erros/` e `/tags/` se o rebuild mudou conteúdo derivado;
6. testar `/docs/` se houve build de documentação;
7. abrir `sitemap.xml` e `robots.txt` quando a alteração afetar URLs;
8. confirmar CSS/JS atualizados e ausência de cache antigo evidente;
9. conferir redirects relevantes;
10. quando a tarefa for de segurança, observar os headers HTTP efetivos.

## Falha de publicação

Se o GitHub contém o commit correto mas o site não mudou, siga [Troubleshooting de webhook](troubleshooting-webhook.md) antes de alterar código ou credenciais sem evidência.

## Registro

Problemas reais resolvidos e reproduzíveis podem ser registrados na Base de Conhecimento — Erros e Soluções. Hipóteses não confirmadas não devem ser apresentadas como causa raiz.
