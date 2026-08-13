# Ambiente local

## Requisitos

O projeto requer Python `>=3.10`. MkDocs e Material for MkDocs são dependências normais; Playwright pertence ao grupo opcional `audit`.

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[audit]"
python -m playwright install chromium
python scripts/install_hooks.py
```

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[audit]"
python -m playwright install chromium
python scripts/install_hooks.py
```

`core.hooksPath` é configuração local, portanto `install_hooks.py` deve ser executado depois de cada clone.

## Verificação inicial

```bash
python -m unittest discover -s tests -v
python scripts/rebuild.py --check
python scripts/build_docs.py --check
python scripts/validate.py
python scripts/validate_docs.py
python scripts/audit_network.py --all
```

## Preview

```bash
python scripts/serve.py
```

Acesse `http://127.0.0.1:8000/`.

## Não versionar

- `.venv/`;
- `__pycache__/`;
- `*.pyc`;
- `*.egg-info/`;
- `dist/`;
- `mkdocs/site/`;
- credenciais, tokens e evidências restritas.
