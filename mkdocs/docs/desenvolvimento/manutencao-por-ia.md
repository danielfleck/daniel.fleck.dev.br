# Manutenção por IA

Ferramentas de IA podem editar o projeto, mas devem respeitar as mesmas fontes de verdade e barreiras de validação usadas por um editor humano.

## Regras obrigatórias

1. O site publicado permanece estático; não introduzir backend, CMS ou banco de conteúdo sem decisão explícita.
2. Em Blog, Portfólio e Erros, preservar `CONTENT-META` e editar o texto somente em `CONTENT-BODY`.
3. Não editar regiões `GENERATED:*` como fonte.
4. Alterar navegação/rodapé em `templates/partials/`.
5. Alterar documentação técnica em `mkdocs/docs/`, não em `site/docs/`.
6. Não inventar fatos, erros, causas, versões ou evidências.
7. Não publicar segredos, IDs administrativos desnecessários, IPs de visitantes, logs individualizados ou documentos restritos.
8. Depois da alteração, executar rebuild, build do MkDocs, validações e testes adequados.

## Erros e Soluções

Quando uma solicitação revelar um problema técnico realmente observado e uma solução confirmada, verifique se já existe registro equivalente em `/erros/`.

- existente → atualizar o registro;
- novo + evidência suficiente → criar registro;
- informação essencial ausente → perguntar ao usuário;
- workaround não comprovado → não chamar de causa raiz.

## Documentos legais

Política de Privacidade e Termos possuem versionamento próprio. Mudança textual exige a regra indicada no próprio documento. Correções puramente estruturais, como consertar um `href` sem alterar a redação jurídica, não incrementam por si mesmas a versão textual.

## Análise ampla

Quando uma IA não consegue navegar recursivamente no repositório, use o pacote gerado por `scripts/package_for_ai.py`. O pacote é temporário e fica em `dist/`.
