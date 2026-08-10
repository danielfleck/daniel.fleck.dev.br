# daniel.fleck.dev.br — site estático multipágina

Esta versão reorganiza o antigo `index.html` monolítico em páginas HTML reais, com URLs próprias para Blog, Portfólio, Base de Conhecimento — Erros e Soluções, Tags, Política de Privacidade e Termos de Uso.

## Princípio de arquitetura

O site publicado contém somente **HTML + CSS + JavaScript estático**. Python não roda na hospedagem: serve exclusivamente para criar novos conteúdos, reconstruir índices/tags/sitemap e validar o repositório antes do commit.

Não há banco de dados de conteúdo e não há arquivo JSON que precise ser editado manualmente. Os metadados ficam no próprio `index.html` de cada conteúdo, em comentário `CONTENT-META`.

## Estrutura

- `index.html`: página inicial/hub.
- `blog/`: índice e posts individuais.
- `portfolio/`: índice e páginas individuais dos projetos/experiências.
- `erros/`: índice e registros da base de erros/soluções.
- `tags/`: páginas geradas automaticamente.
- `privacidade/` e `termos/`: documentos jurídicos independentes.
- `templates/`: modelos e parciais compartilhados.
- `scripts/`: ferramentas locais Python.
- `docs/AI-MAINTENANCE.md`: procedimento para edição humana/IA.
- `docs/STRUCTURE.md`: árvore e fontes de verdade da arquitetura.
- `docs/VALIDATION.md`: verificações executadas na migração inicial.

## Ambiente local

```bash
python3 -m venv .venv
source .venv/bin/activate
python scripts/rebuild.py
python scripts/validate.py
python -m unittest discover -s tests
```

Não existem dependências Python externas.

## Instalar o hook do Git

Após `git init` ou clone:

```bash
python scripts/install_hooks.py
```

O `pre-commit` executa o rebuild. Se o rebuild alterar páginas geradas, o commit é interrompido para que você revise e faça `git add -A`; depois basta repetir o commit. Se não houver alterações geradas, a validação é executada e o commit segue.

## Criar novo conteúdo

### Blog

```bash
python scripts/create_content.py blog
```

### Portfólio

```bash
python scripts/create_content.py portfolio
```

### Base de Conhecimento — Erros e Soluções

```bash
python scripts/create_content.py erro
```

O script pergunta título, resumo, data, slug, categoria/status e tags; cria a pasta e o `index.html` a partir do template; depois executa rebuild. Edite somente o trecho entre `CONTENT-BODY:START` e `CONTENT-BODY:END`.

## Rebuild

```bash
python scripts/rebuild.py
```

Ele lê `CONTENT-META` das páginas existentes e atualiza automaticamente:

- cabeçalho e metadados SEO de cada conteúdo;
- JSON-LD;
- `/blog/index.html`;
- `/portfolio/index.html`;
- `/erros/index.html`;
- destaques da home;
- nuvem de tags;
- `/tags/` e páginas de cada tag;
- `sitemap.xml`;
- navegação e rodapé compartilhados.

## Validação aprofundada

`python scripts/validate.py` também verifica canonical único, meta description, H1, JSON-LD, placeholders não resolvidos, links/recursos locais, sitemap, recursos externos automáticos e atualização do rebuild.

## Preview local

```bash
python scripts/serve.py
```

Abra `http://127.0.0.1:8000/`.

## Como entregar o site inteiro a uma IA

Você não precisa anexar dezenas de páginas uma a uma. Há três opções:

1. **Análise do conteúdo publicado:** forneça `https://daniel.fleck.dev.br/` e `https://daniel.fleck.dev.br/sitemap.xml`.
2. **Análise do código:** forneça `https://github.com/danielfleck/daniel.fleck.dev.br` a uma IA que consiga navegar no GitHub.
3. **Mais confiável:** execute `python scripts/package_for_ai.py` e envie o único arquivo `dist/site-for-ai.zip`.

A opção 3 evita depender da capacidade de crawler da IA e garante que templates, scripts e arquivos não públicos do repositório também sejam analisados.

## Observação sobre `jira1.png`

O HTML original referenciava `images/jira1.png`, mas o binário não estava disponível entre os arquivos usados nesta migração. Para que o pacote não tenha imagem quebrada, foi incluído `images/jira1-placeholder.svg`. Antes de publicar, substitua pela captura original existente no repositório, se desejar preservar a evidência visual.
