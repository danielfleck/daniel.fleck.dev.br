# Validação da migração multipágina — 10/08/2026

Esta página registra a validação realizada na geração inicial da arquitetura estática multipágina. Não substitui as validações executadas a cada alteração.

## Estado validado

- 10 posts de Blog.
- 6 itens de Portfólio.
- 1 registro em Erros e Soluções.
- 59 tags e respectivas páginas estáticas.
- 87 arquivos HTML públicos no conjunto validado, dos quais 86 constam no sitemap (a página 404 é excluída).
- Política de Privacidade preservada na versão 4.
- Termos de Uso preservados na versão 3.

## Verificações executadas

```bash
python scripts/rebuild.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
node --check js/main.js
```

Também foram testados:

- ambiente `.venv` limpo, sem dependências Python externas;
- criação interativa de Blog, Portfólio e Erro, seguida de rebuild e validação;
- campo `featured` do Portfólio;
- hook `pre-commit`, inclusive o bloqueio do commit quando o rebuild gera mudanças não revisadas;
- servidor HTTP local e resposta 200 para home, índices, conteúdos, tags, documentos legais, currículo, CSS, JavaScript e sitemap;
- unicidade de `<title>`, canonical e meta description nas páginas públicas;
- parse de JSON-LD e sitemap XML;
- consistência de links e recursos locais;
- ausência de scripts, imagens, iframes e folhas de estilo carregados automaticamente de terceiros;
- preservação textual do conteúdo jurídico ao separar Política e Termos do antigo `index.html`.

## Observação sobre imagem

A captura original `images/jira1.png` não estava disponível no conjunto de arquivos utilizado para esta migração. O pacote usa `images/jira1-placeholder.svg` para não gerar referência quebrada. Substitua pelo arquivo original antes da publicação se quiser manter essa evidência visual.
