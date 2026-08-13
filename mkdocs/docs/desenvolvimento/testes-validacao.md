# Testes e validação

A validação é uma barreira contra regressões introduzidas por edição manual, scripts ou ferramentas de IA.

## Testes automatizados

```bash
python -m unittest discover -s tests -v
```

São especialmente importantes após mudanças em parsing de metadados, geração de URLs, tags, build ou validação.

## Validação do site

```bash
python scripts/validate.py
```

Deve verificar, conforme a implementação vigente:

- metadados obrigatórios;
- duplicidade de conteúdos;
- colisão de slugs;
- `<title>`, `<h1>`, canonical e description;
- JSON-LD válido;
- links e recursos locais;
- sitemap;
- placeholders não resolvidos;
- recursos externos automáticos proibidos;
- estado atualizado do rebuild.

## Validação da documentação

```bash
python scripts/validate_docs.py
```

O MkDocs é validado separadamente porque o Material gera HTML próprio e utiliza JavaScript inline. A validação não deve aplicar cegamente as mesmas regras de template do site principal.

Para uma verificação opcional de headers no ambiente publicado:

```bash
python scripts/validate_docs.py --production-url https://daniel.fleck.dev.br/docs/
```

## Inspeção visual

```bash
python scripts/serve.py
```

Revise no mínimo home, páginas alteradas, navegação mobile quando relevante, `/docs/`, Política e Termos se componentes compartilhados tiverem mudado.
