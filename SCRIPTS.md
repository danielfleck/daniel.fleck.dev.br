# Guia dos scripts de manutenção do site

Este documento explica para que serve cada script Python do projeto e qual é a sequência mais comum de uso no dia a dia.

> **Importante:** o site publicado continua sendo totalmente estático.  
> Python é usado somente no ambiente local de desenvolvimento para criar conteúdo, reconstruir arquivos derivados, validar o projeto, executar testes e preparar pacotes auxiliares.

---

## 1. Preparação do ambiente

O projeto requer **Python 3.11 ou superior** e, atualmente, não possui dependências externas.

Na primeira utilização:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

O `pyproject.toml` declara:

```text
requires-python = ">=3.11"
dependencies = []
```

Portanto, não é necessário instalar pacotes com `pip` no estado atual do projeto.

Depois de criar a `.venv`, configure os hooks do Git uma vez:

```bash
python scripts/install_hooks.py
```

Essa configuração deve ser repetida após cada novo clone do repositório, porque `core.hooksPath` é uma configuração local do Git.

---

# 2. Sequência mais comum no dia a dia

Na maioria das alterações, o fluxo recomendado é:

```text
ATIVAR .venv
    ↓
EDITAR CONTEÚDO OU CÓDIGO
    ↓
REBUILD
    ↓
VALIDATE
    ↓
SERVE / REVISÃO VISUAL
    ↓
GIT DIFF
    ↓
GIT ADD
    ↓
GIT COMMIT
    ↓
PRE-COMMIT CONFERE NOVAMENTE
    ↓
GIT PUSH
```

Em comandos:

```bash
source .venv/bin/activate

# faça a edição desejada

python scripts/rebuild.py
python scripts/validate.py
python scripts/serve.py

git status
git diff
git add -A
git commit -m "Descrição da alteração"
git push
```

`serve.py` é opcional quando a alteração não exige inspeção visual.

---

# 3. Alterar um conteúdo já existente

Exemplos:

```text
blog/<slug>/index.html
portfolio/<slug>/index.html
erros/<slug>/index.html
```

Nos conteúdos individuais, o texto editorial deve permanecer entre:

```html
<!-- CONTENT-BODY:START -->

...conteúdo...

<!-- CONTENT-BODY:END -->
```

Evite editar manualmente regiões delimitadas por:

```html
<!-- GENERATED:...:START -->
...
<!-- GENERATED:...:END -->
```

Essas regiões são reconstruídas automaticamente por `rebuild.py`.

Depois da edição:

```bash
python scripts/rebuild.py
python scripts/validate.py
```

Para conferir no navegador:

```bash
python scripts/serve.py
```

Depois:

```bash
git diff
git add -A
git commit -m "Atualiza ..."
git push
```

---

# 4. Criar um novo post do Blog

Execute:

```bash
python scripts/create_content.py blog
```

O script solicita:

- título;
- resumo;
- data no formato `AAAA-MM-DD`;
- slug;
- categoria;
- tags.

Ele:

1. lê `templates/blog.html`;
2. cria `blog/<slug>/index.html`;
3. preenche os metadados;
4. executa automaticamente `rebuild.py`.

Depois, edite apenas o corpo editorial:

```html
<!-- CONTENT-BODY:START -->
...
<!-- CONTENT-BODY:END -->
```

Ao terminar:

```bash
python scripts/rebuild.py
python scripts/validate.py
python scripts/serve.py
```

Fluxo resumido:

```text
create_content.py blog
        ↓
novo index.html do post
        ↓
editar CONTENT-BODY
        ↓
rebuild.py
        ↓
validate.py
        ↓
serve.py (opcional)
        ↓
git diff
        ↓
commit
```

---

# 5. Criar um novo item de Portfólio

Execute:

```bash
python scripts/create_content.py portfolio
```

O template usado é:

```text
templates/portfolio.html
```

O arquivo é criado em:

```text
portfolio/<slug>/index.html
```

Além dos metadados comuns, o script pergunta:

```text
Destacar na página inicial? (s/n)
```

Depois de preencher o conteúdo:

```bash
python scripts/rebuild.py
python scripts/validate.py
python scripts/serve.py
```

---

# 6. Criar um registro em Erros e Soluções

Execute:

```bash
python scripts/create_content.py erro
```

O template usado é:

```text
templates/erro.html
```

O arquivo será criado em:

```text
erros/<slug>/index.html
```

O script também solicita o campo `status`, cujo valor padrão é:

```text
Resolvido
```

Essa seção deve distinguir claramente:

- contexto;
- problema observado;
- evidência;
- diagnóstico;
- hipótese, quando houver;
- solução aplicada;
- resultado;
- aprendizado.

Não registre hipótese como causa comprovada.

Depois:

```bash
python scripts/rebuild.py
python scripts/validate.py
```

---

# 7. `scripts/create_content.py`

## Finalidade

Cria conteúdo novo a partir dos templates existentes.

Tipos aceitos:

```bash
python scripts/create_content.py blog
python scripts/create_content.py portfolio
python scripts/create_content.py erro
```

## O que ele faz

- valida título e resumo;
- valida a data ISO;
- gera ou normaliza o slug;
- exige pelo menos uma tag;
- impede metadados que quebrem o comentário `CONTENT-META`;
- impede sobrescrever um slug já existente;
- seleciona o template correto;
- cria a pasta e o `index.html`;
- executa `rebuild.py`.

## Observação importante

O script cria o esqueleto e os metadados, mas o conteúdo principal deve ser editado depois no bloco `CONTENT-BODY`.

---

# 8. `scripts/rebuild.py`

## Finalidade

É o principal script de geração do site.

Ele lê os metadados das páginas-fonte existentes em:

```text
blog/*/index.html
portfolio/*/index.html
erros/*/index.html
```

e reconstrói artefatos derivados.

Entre as tarefas estão:

- navegação compartilhada;
- rodapé compartilhado;
- cabeçalho das páginas de conteúdo;
- SEO;
- JSON-LD;
- `/blog/index.html`;
- `/portfolio/index.html`;
- `/erros/index.html`;
- cards derivados da página inicial;
- nuvem de tags;
- `/tags/index.html`;
- `/tags/<tag>/index.html`;
- `sitemap.xml`;
- `robots.txt`.

## Uso normal

```bash
python scripts/rebuild.py
```

O script só grava arquivos quando o resultado realmente mudou.

Se tudo estiver atualizado:

```text
Rebuild: nenhum arquivo gerado precisou ser alterado.
```

## Verificar sem modificar

```bash
python scripts/rebuild.py --check
```

Nesse modo ele não grava nada.

Códigos de saída:

- `0`: tudo atualizado;
- `2`: existem artefatos que precisariam ser reconstruídos.

## Modo do hook Git

```bash
python scripts/rebuild.py --hook
```

Normalmente não deve ser executado manualmente.

Se o rebuild alterar arquivos durante o `pre-commit`, o script retorna código `3` para interromper o commit e permitir revisão.

---

# 9. `scripts/validate.py`

## Finalidade

Executa verificações estruturais, de SEO e de integridade.

Comando:

```bash
python scripts/validate.py
```

Entre as verificações estão:

- metadados obrigatórios;
- duplicidade de conteúdos;
- colisão de slugs de tags;
- presença dos marcadores de manutenção;
- `<h1>`;
- `<title>`;
- canonical;
- meta description;
- JSON-LD válido;
- links e recursos internos;
- sitemap;
- ausência de placeholders não resolvidos;
- ausência de recursos externos carregados automaticamente;
- ausência de imagens `data:`/base64;
- estado atualizado do rebuild.

Quando tudo estiver correto:

```text
VALIDAÇÃO OK: ...
```

Se houver erro, retorna código diferente de zero.

## Quando executar

Recomendado:

- depois de uma alteração;
- antes de publicar;
- antes de um commit importante;
- depois de uma alteração feita por IA;
- depois de mudanças em scripts Python.

---

# 10. `scripts/serve.py`

## Finalidade

Inicia um servidor HTTP local usando apenas a biblioteca padrão do Python.

Comando:

```bash
python scripts/serve.py
```

URL:

```text
http://127.0.0.1:8000/
```

Use para revisar:

- navegação;
- layout;
- CSS;
- JavaScript;
- blog;
- portfólio;
- erros;
- tags;
- páginas legais.

Para encerrar:

```text
Ctrl+C
```

Para testes locais, prefira esse servidor a abrir o HTML diretamente por `file://`.

---

# 11. `scripts/install_hooks.py`

## Finalidade

Configura o Git para usar os hooks versionados em:

```text
.githooks/
```

Execute:

```bash
python scripts/install_hooks.py
```

Isso configura:

```text
core.hooksPath = .githooks
```

e garante permissão de execução para o hook.

## Quando usar

Execute uma vez:

- após clonar o projeto;
- ao configurar o projeto em outra máquina;
- se a configuração local dos hooks for perdida.

---

# 12. Hook `.githooks/pre-commit`

O hook não é Python, mas faz parte do fluxo.

Quando você executa:

```bash
git commit
```

ele procura o Python nesta ordem:

```text
.venv/bin/python
.venv/Scripts/python.exe
python3
```

Depois:

```text
1. executa rebuild.py --hook
2. se o rebuild alterar arquivos, interrompe o commit
3. você revisa e adiciona os arquivos gerados
4. repete o commit
5. se não houver rebuild pendente, executa validate.py
6. o commit só continua se a validação for aprovada
```

Se o commit for interrompido porque o rebuild criou mudanças:

```bash
git status
git diff
git add -A
git commit -m "Descrição"
```

Isso é intencional: o hook não faz `git add` automaticamente.

---

# 13. `scripts/package_for_ai.py`

## Finalidade

Gera um ZIP compacto do projeto para análise por ChatGPT ou outra IA.

Execute:

```bash
python scripts/package_for_ai.py
```

Resultado:

```text
dist/site-for-ai.zip
```

Também gera:

```text
dist/AI_INDEX.md
```

O pacote ignora itens locais ou derivados que não ajudam na análise:

```text
.git/
.venv/
dist/
__pycache__/
```

## Quando usar

Use para pedir a uma IA:

- revisão global do site;
- busca por inconsistências;
- análise de SEO;
- revisão de referências cruzadas;
- análise de navegação;
- alterações que possam afetar vários arquivos.

Em vez de enviar dezenas de arquivos, envie:

```text
dist/site-for-ai.zip
```

Esse ZIP é apenas um artefato de análise. A fonte oficial continua sendo o repositório Git.

---

# 14. `scripts/site_config.py`

Este arquivo não é normalmente executado diretamente.

Ele guarda configurações globais utilizadas pelos scripts, atualmente:

```python
BASE_URL = "https://daniel.fleck.dev.br"
AUTHOR = "Daniel Rodrigo Fleck"
```

Se domínio ou dados globais mudarem, revise esse arquivo.

Depois:

```bash
python scripts/rebuild.py
python scripts/validate.py
```

---

# 15. `scripts/site_utils.py`

Também não deve ser executado diretamente.

Contém funções e estruturas compartilhadas pelos demais scripts.

Entre suas responsabilidades:

- estrutura `ContentMeta`;
- leitura de `CONTENT-META`;
- descoberta dos conteúdos;
- geração e normalização de slugs;
- slugs de tags;
- links HTML de tags;
- substituição de regiões `GENERATED`;
- resolução de links e recursos locais para validação.

Alterações nele podem repercutir em vários scripts.

Depois de modificar `site_utils.py`, execute:

```bash
python -m unittest discover -s tests -v
python scripts/rebuild.py
python scripts/validate.py
```

---

# 16. `scripts/__init__.py`

Não é um comando.

Serve para identificar e documentar a pasta `scripts` como pacote Python do projeto.

Normalmente não precisa ser alterado.

---

# 17. Testes automatizados

Os testes ficam em:

```text
tests/
```

Execute todos com:

```bash
python -m unittest discover -s tests -v
```

É especialmente recomendado depois de mudanças em:

```text
scripts/rebuild.py
scripts/site_utils.py
scripts/create_content.py
scripts/validate.py
```

Para uma alteração puramente textual em um post, normalmente `rebuild.py` + `validate.py` são suficientes.

---

# 18. Fluxos rápidos

## Corrigir um post existente

```bash
source .venv/bin/activate

# editar blog/<slug>/index.html

python scripts/rebuild.py
python scripts/validate.py
python scripts/serve.py

git diff
git add -A
git commit -m "Corrige post ..."
git push
```

---

## Criar post novo

```bash
source .venv/bin/activate

python scripts/create_content.py blog

# editar blog/<slug>/index.html

python scripts/rebuild.py
python scripts/validate.py
python scripts/serve.py

git diff
git add -A
git commit -m "Adiciona post ..."
git push
```

---

## Criar item de portfólio

```bash
source .venv/bin/activate

python scripts/create_content.py portfolio

# editar portfolio/<slug>/index.html

python scripts/rebuild.py
python scripts/validate.py
python scripts/serve.py

git diff
git add -A
git commit -m "Adiciona item ao portfólio ..."
git push
```

---

## Registrar um problema resolvido

```bash
source .venv/bin/activate

python scripts/create_content.py erro

# editar erros/<slug>/index.html

python scripts/rebuild.py
python scripts/validate.py
python scripts/serve.py

git diff
git add -A
git commit -m "Documenta erro ..."
git push
```

---

## Alterar CSS, JavaScript ou layout

```bash
source .venv/bin/activate

# editar arquivos

python scripts/rebuild.py
python scripts/validate.py
python scripts/serve.py

git diff
git add -A
git commit -m "Ajusta layout ..."
git push
```

---

## Modificar scripts Python

```bash
source .venv/bin/activate

# editar scripts/*.py

python -m unittest discover -s tests -v
python scripts/rebuild.py
python scripts/validate.py
python scripts/serve.py

git diff
git add -A
git commit -m "Ajusta scripts de build ..."
git push
```

---

## Preparar pacote para análise por IA

```bash
source .venv/bin/activate

python scripts/rebuild.py
python scripts/validate.py
python scripts/package_for_ai.py
```

Depois envie:

```text
dist/site-for-ai.zip
```

---

# 19. Tabela de referência rápida

| Situação | Comando |
|---|---|
| Criar post do Blog | `python scripts/create_content.py blog` |
| Criar item de Portfólio | `python scripts/create_content.py portfolio` |
| Criar registro de Erro/Solução | `python scripts/create_content.py erro` |
| Reconstruir índices, tags, SEO e sitemap | `python scripts/rebuild.py` |
| Conferir rebuild sem gravar | `python scripts/rebuild.py --check` |
| Validar todo o site | `python scripts/validate.py` |
| Abrir site localmente | `python scripts/serve.py` |
| Configurar hook após clone | `python scripts/install_hooks.py` |
| Gerar ZIP para IA | `python scripts/package_for_ai.py` |
| Executar testes | `python -m unittest discover -s tests -v` |

---

# 20. O que evitar

Não faça manualmente aquilo que os scripts já gerenciam.

Evite:

- editar regiões `GENERATED`;
- editar páginas de tags geradas;
- editar `sitemap.xml` manualmente;
- editar índices gerados sem alterar a fonte correspondente;
- criar conteúdo novo sem `CONTENT-META`;
- ignorar uma falha de `validate.py`;
- usar `site-for-ai.zip` como fonte oficial;
- versionar `.venv`;
- colocar Python na hospedagem;
- fazer `git add` automático dentro de scripts de manutenção sem revisão.

---

# 21. Regra prática antes de um commit

Se quiser uma rotina curta e segura:

```bash
python scripts/rebuild.py
python scripts/validate.py
git status
git diff
git add -A
git commit -m "Descrição"
git push
```

Se a alteração for visual, inclua antes do commit:

```bash
python scripts/serve.py
```

Se a alteração envolver os próprios scripts Python, inclua também:

```bash
python -m unittest discover -s tests -v
```

---

# 22. Em caso de dúvida sobre impacto de uma alteração

Primeiro confirme que o projeto atual está consistente:

```bash
python scripts/rebuild.py --check
python scripts/validate.py
```

Se a alteração puder afetar muitos arquivos e você quiser análise por IA:

```bash
python scripts/package_for_ai.py
```

e forneça:

```text
dist/site-for-ai.zip
```

junto com a descrição da alteração desejada.
