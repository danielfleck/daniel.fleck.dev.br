# Templates e partials

Templates permitem criar novos conteúdos com uma estrutura previsível e partials mantêm componentes compartilhados coerentes entre as páginas.

## Templates de conteúdo

```text
templates/blog.html
templates/portfolio.html
templates/erro.html
```

Os templates contêm placeholders substituídos por `create_content.py`, o bloco `CONTENT-META`, marcadores de corpo editorial e regiões geradas.

Ao alterar um template, lembre-se de que a mudança afeta **novos conteúdos**. Se a alteração também precisar atingir páginas já existentes, implemente-a no rebuild, em partial compartilhado ou numa migração explícita e revisável.

## Partials

`templates/partials/nav.html` e `templates/partials/footer.html` são fontes dos componentes compartilhados. `rebuild.py` replica essas estruturas nas páginas que possuem marcadores correspondentes.

Não edite manualmente a navegação copiada em dezenas de HTMLs. Altere o partial e execute o rebuild.

## Marcadores

Regiões como:

```html
<!-- GENERATED:SITE-NAV:START -->
...
<!-- GENERATED:SITE-NAV:END -->
```

são sobrescritas. A fonte está no partial ou no gerador associado.

## Revisão

Depois de alterar templates ou partials:

```bash
python scripts/rebuild.py
python scripts/validate.py
python scripts/serve.py
```

Revise `git diff` para garantir que a mudança propagada corresponde ao objetivo e não modificou conteúdo editorial não relacionado.
