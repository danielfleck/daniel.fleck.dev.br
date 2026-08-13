# Ambiente local

## Requisitos

O projeto requer Python `>=3.10`. As dependências declaradas no `pyproject.toml` incluem MkDocs e Material for MkDocs.

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Depois de cada clone:

```bash
python scripts/install_hooks.py
```

O hook é configuração local do Git; portanto, clonar o repositório não ativa automaticamente `core.hooksPath`.

## Comandos de verificação inicial

```bash
python scripts/rebuild.py --check
python scripts/build_docs.py --check
python scripts/validate.py
python scripts/validate_docs.py
python -m unittest discover -s tests -v
```

## Preview

```bash
python scripts/serve.py
```

Acesse `http://127.0.0.1:8000/`. Prefira servidor HTTP local a abrir páginas por `file://`, pois caminhos absolutos e comportamento de navegação são testados de maneira mais próxima da publicação real.

## O que não deve ser versionado

- `.venv/`;
- `__pycache__/`;
- `*.pyc`;
- `*.egg-info/`;
- `dist/`;
- `mkdocs/site/`;
- segredos e arquivos locais não previstos no projeto.
