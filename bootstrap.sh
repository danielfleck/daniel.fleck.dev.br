#!/usr/bin/env bash
set -Eeuo pipefail

BASE_URL="${BASE_URL:-https://daniel.fleck.dev.br}"
DOCS_URL="${DOCS_URL:-${BASE_URL%/}/docs/}"

info() { printf '\n==> %s\n' "$*"; }
warn() { printf '\nWARN: %s\n' "$*" >&2; }
die() { printf '\nERRO: %s\n' "$*" >&2; exit 1; }

on_error() {
	    code=$?
	        printf '\nERRO: bootstrap interrompido (código %s).\n' "$code" >&2
		    exit "$code"
	    }
	    trap on_error ERR

	    ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
	    cd "$ROOT"

	    info "Conferindo repositório"
	    git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "execute este script dentro do repositório Git."
	    [[ -f pyproject.toml ]] || die "pyproject.toml não encontrado."
	    [[ -d scripts ]] || die "pasta scripts/ não encontrada."

	    HEAD_SHA="$(git rev-parse HEAD)"
	    HEAD_SHORT="$(git rev-parse --short HEAD)"
	    printf 'Commit atual: %s\n' "$HEAD_SHA"

	    if command -v python3 >/dev/null 2>&1; then
		        BOOTSTRAP_PY="$(command -v python3)"
		elif command -v python >/dev/null 2>&1; then
			    BOOTSTRAP_PY="$(command -v python)"
		    else
			        die "Python não encontrado no PATH."
			fi

			info "Conferindo versão do Python"
			"$BOOTSTRAP_PY" - <<'PY'
import sys
print("Python:", sys.version.split()[0])
if sys.version_info[:2] < (3, 9):
    raise SystemExit("ERRO: Python 3.9 ou superior é necessário.")
PY

if [[ ! -d .venv ]]; then
	    info "Criando ambiente virtual .venv"
	        "$BOOTSTRAP_PY" -m venv .venv
	else
		    info "Ambiente virtual .venv já existe; reutilizando"
	    fi

	    PY="$ROOT/.venv/bin/python"
	    [[ -x "$PY" ]] || die ".venv/bin/python não foi criado corretamente."

	    info "Atualizando pip e setuptools"
	    "$PY" -m pip install --upgrade pip setuptools

	    info "Instalando projeto e dependências de auditoria"
	    "$PY" -m pip install -e ".[audit]"

	    info "Conferindo Playwright"
	    "$PY" -c "import playwright; print('Playwright Python: OK')"
	    "$PY" -m playwright --version

	    info "Instalando/confirmando Chromium do Playwright"
	    "$PY" -m playwright install chromium

	    info "Ativando hooks Git"
	    "$PY" scripts/install_hooks.py

	    HOOKS_PATH="$(git config --get core.hooksPath || true)"
	    [[ "$HOOKS_PATH" == ".githooks" ]] || die "core.hooksPath deveria ser .githooks; recebido: ${HOOKS_PATH:-<vazio>}."

	    info "Executando testes"
	    "$PY" -m unittest discover -s tests -v

	    info "Validando site local"
	    "$PY" scripts/validate.py

	    info "Validando MkDocs local"
	    "$PY" scripts/validate_docs.py

	    info "Validando contato"
	    "$PY" scripts/validate_contact_surface.py

	    info "Validando documentos legais"
	    "$PY" scripts/validate_legal_rationale.py

	    info "Validando transporte local"
	    "$PY" scripts/validate_transport_security.py

	    info "Executando auditoria headless local"
	    "$PY" scripts/audit_network.py --all

	    info "Validando produção sem cache"
	    "$PY" scripts/validate_production_nocache.py --base-url "$BASE_URL"

	    info "Validando transporte em produção"
	    "$PY" scripts/validate_transport_security.py --production-url "$BASE_URL"

	    info "Validando produção com auditoria de rede"
	    "$PY" scripts/validate.py --production-url "$BASE_URL" --network

	    info "Validando MkDocs publicado"
	    "$PY" scripts/validate_docs.py --production-url "$DOCS_URL"

	    info "Conferindo superfícies administrativas"
	    "$PY" scripts/check_admin_surfaces.py --base-url "$BASE_URL"

	    if command -v dig >/dev/null 2>&1; then
		        info "Conferindo SPF e DMARC"
			    "$PY" scripts/check_email_dns.py
		    else
			        warn "comando dig não encontrado; check_email_dns.py não foi executado."
			fi

			info "Conferindo alterações em arquivos rastreados"
			if ! git diff --quiet || ! git diff --cached --quiet; then
				    git status --short
				        die "há alterações em arquivos rastreados após o bootstrap; revise antes de continuar."
				fi

				info "Bootstrap concluído"
				printf 'Commit validado: %s (%s)\n' "$HEAD_SHORT" "$HEAD_SHA"
				printf 'Produção: %s\n' "$BASE_URL"
				printf 'Hooks Git: %s\n' "$HOOKS_PATH"
				printf '\nPara ativar o ambiente virtual na sessão atual:\n'
				printf '  source .venv/bin/activate\n'

