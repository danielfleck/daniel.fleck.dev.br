"""Audita requisições de rede feitas pelo site em um navegador Chromium headless.

Objetivo
--------
Detectar requisições HTTP/HTTPS/WS/WSS feitas em tempo de execução para
hosts fora do domínio permitido. Diferentemente de uma busca textual por
``src="https://..."``, este script observa as requisições que o JavaScript
realmente tenta executar.

Por segurança, requisições para hosts não permitidos são registradas e
abortadas antes de serem efetivamente enviadas.

Uso rápido
----------
Auditoria local de todo o conteúdo gerado em ``site/``::

    python scripts/audit_network.py --all

Auditoria do site já publicado::

    python scripts/audit_network.py \
        --base-url https://daniel.fleck.dev.br \
        --all \
        --report dist/network-audit-production.json

Dependência
-----------
Requer Playwright e o Chromium gerenciado pelo Playwright::

    python -m pip install -e ".[audit]"
    python -m playwright install chromium
"""

from __future__ import annotations

import argparse
import json
import threading
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

from site_config import BASE_URL
from site_utils import PROJECT_ROOT, SITE_ROOT


DEFAULT_REPORT = PROJECT_ROOT / "dist" / "network-audit.json"
NON_NETWORK_SCHEMES = {"about", "blob", "data"}
NETWORK_SCHEMES = {"http", "https", "ws", "wss"}

# Páginas representativas para uma auditoria rápida.
QUICK_PATHS = (
    "/",
    "/blog/",
    "/portfolio/",
    "/erros/",
    "/privacidade/",
    "/termos/",
    "/docs/",
)


@dataclass(frozen=True)
class RequestRecord:
    page: str
    method: str
    resource_type: str
    url: str
    scheme: str
    host: str
    allowed: bool


class QuietHandler(SimpleHTTPRequestHandler):
    """Servidor local sem ruído de log a cada requisição."""

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return


def public_path_for_html(path: Path) -> str:
    """Converte um HTML de ``site/`` em URL pública."""

    relative = path.relative_to(SITE_ROOT)
    if relative.name == "index.html":
        parent = relative.parent.as_posix()
        return "/" if parent == "." else f"/{parent.strip('/')}/"
    return "/" + relative.as_posix()


def discover_public_paths() -> list[str]:
    """Retorna todas as URLs HTML presentes no build público."""

    paths = {public_path_for_html(path) for path in SITE_ROOT.rglob("*.html")}
    return sorted(paths, key=lambda value: (value != "/", value))


def normalize_host(host: str) -> str:
    return host.strip().lower().rstrip(".")


def host_is_allowed(
    host: str,
    *,
    exact_hosts: set[str],
    suffixes: set[str],
) -> bool:
    """Confere host exato ou subdomínio explicitamente autorizado."""

    candidate = normalize_host(host)
    if candidate in exact_hosts:
        return True

    for suffix in suffixes:
        suffix = normalize_host(suffix).lstrip(".")
        if candidate == suffix or candidate.endswith("." + suffix):
            return True

    return False


def start_local_server() -> tuple[ThreadingHTTPServer, threading.Thread, str]:
    """Serve ``site/`` em uma porta local livre."""

    handler = partial(QuietHandler, directory=str(SITE_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{port}"


def select_paths(args: argparse.Namespace) -> list[str]:
    if args.path:
        return sorted(set(args.path))

    if args.all:
        return discover_public_paths()

    available = set(discover_public_paths())
    selected = [path for path in QUICK_PATHS if path in available]
    return selected or ["/"]


def ensure_leading_slash(path: str) -> str:
    if not path.startswith("/"):
        return "/" + path
    return path


def write_report(
    path: Path,
    *,
    base_url: str,
    allowed_hosts: set[str],
    allowed_suffixes: set[str],
    pages: list[str],
    records: list[RequestRecord],
    navigation_errors: list[dict[str, str]],
) -> None:
    violations = [record for record in records if not record.allowed]

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "base_url": base_url,
        "allowed_hosts": sorted(allowed_hosts),
        "allowed_subdomain_suffixes": sorted(allowed_suffixes),
        "pages_audited": pages,
        "request_count": len(records),
        "violation_count": len(violations),
        "navigation_error_count": len(navigation_errors),
        "violations": [asdict(record) for record in violations],
        "navigation_errors": navigation_errors,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def audit(args: argparse.Namespace) -> int:
    if not SITE_ROOT.is_dir():
        print(f"ERRO: raiz pública não encontrada: {SITE_ROOT}")
        return 2

    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERRO: Playwright não está instalado.")
        print('Execute: python -m pip install -e ".[audit]"')
        print("Depois:  python -m playwright install chromium")
        return 2

    local_server = None
    if args.base_url:
        base_url = args.base_url.rstrip("/")
    else:
        local_server, _thread, base_url = start_local_server()

    parsed_base = urlparse(base_url)
    if parsed_base.scheme not in {"http", "https"} or not parsed_base.hostname:
        if local_server:
            local_server.shutdown()
            local_server.server_close()
        print(f"ERRO: base URL inválida: {base_url}")
        return 2

    exact_hosts = {
        normalize_host(parsed_base.hostname),
        normalize_host(urlparse(BASE_URL).hostname or ""),
    }
    exact_hosts.discard("")
    exact_hosts.update(normalize_host(value) for value in args.allow_host)

    allowed_suffixes = {
        normalize_host(value).lstrip(".")
        for value in args.allow_subdomains_of
        if value.strip()
    }

    paths = [ensure_leading_slash(path) for path in select_paths(args)]
    report_path = Path(args.report)
    if not report_path.is_absolute():
        report_path = PROJECT_ROOT / report_path

    records: list[RequestRecord] = []
    navigation_errors: list[dict[str, str]] = []
    current_page = {"url": ""}

    def classify(url: str) -> tuple[bool, str, str]:
        parsed = urlparse(url)
        scheme = parsed.scheme.lower()

        if scheme in NON_NETWORK_SCHEMES:
            return True, scheme, ""

        if scheme not in NETWORK_SCHEMES:
            # Recursos internos do navegador não representam uma chamada
            # HTTP/HTTPS a terceiro.
            return True, scheme, normalize_host(parsed.hostname or "")

        host = normalize_host(parsed.hostname or "")
        allowed = host_is_allowed(
            host,
            exact_hosts=exact_hosts,
            suffixes=allowed_suffixes,
        )
        return allowed, scheme, host

    try:
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=True)
            except PlaywrightError as exc:
                print("ERRO: Chromium do Playwright não está disponível.")
                print("Execute: python -m playwright install chromium")
                print(f"Detalhe: {exc}")
                return 2

            context = browser.new_context(
                java_script_enabled=True,
                service_workers="block",
            )

            def route_handler(route) -> None:
                request = route.request
                allowed, scheme, host = classify(request.url)

                records.append(
                    RequestRecord(
                        page=current_page["url"],
                        method=request.method,
                        resource_type=request.resource_type,
                        url=request.url,
                        scheme=scheme,
                        host=host,
                        allowed=allowed,
                    )
                )

                if not allowed and scheme in NETWORK_SCHEMES:
                    # A violação é detectada, mas a requisição é interrompida
                    # antes de efetivamente alcançar o terceiro.
                    route.abort("blockedbyclient")
                else:
                    route.continue_()

            context.route("**/*", route_handler)
            page = context.new_page()

            for path in paths:
                url = urljoin(base_url + "/", path.lstrip("/"))
                current_page["url"] = url

                try:
                    page.goto(
                        url,
                        wait_until="load",
                        timeout=args.timeout_ms,
                    )
                    # Requisições dinâmicas do Material são disparadas logo
                    # após a inicialização. Este pequeno período permite
                    # capturar tarefas assíncronas sem usar time.sleep().
                    page.wait_for_timeout(args.settle_ms)
                except PlaywrightError as exc:
                    navigation_errors.append(
                        {"page": url, "error": str(exc)}
                    )

            context.close()
            browser.close()
    finally:
        if local_server:
            local_server.shutdown()
            local_server.server_close()

    violations = [record for record in records if not record.allowed]
    write_report(
        report_path,
        base_url=base_url,
        allowed_hosts=exact_hosts,
        allowed_suffixes=allowed_suffixes,
        pages=paths,
        records=records,
        navigation_errors=navigation_errors,
    )

    print(f"Páginas auditadas: {len(paths)}")
    print(f"Requisições observadas: {len(records)}")
    print(f"Relatório: {report_path.relative_to(PROJECT_ROOT) if report_path.is_relative_to(PROJECT_ROOT) else report_path}")

    if navigation_errors:
        print("\nERROS DE NAVEGAÇÃO")
        for error in navigation_errors:
            print(f"- {error['page']}: {error['error']}")

    if violations:
        print("\nAUDITORIA DE REDE FALHOU")
        grouped: dict[str, list[RequestRecord]] = {}
        for record in violations:
            grouped.setdefault(record.host or record.scheme, []).append(record)

        for host, items in sorted(grouped.items()):
            print(f"- Host não permitido: {host}")
            for item in items[:10]:
                print(
                    f"  {item.method} {item.url} "
                    f"[{item.resource_type}] em {item.page}"
                )
            if len(items) > 10:
                print(f"  ... e mais {len(items) - 10} requisições")

        return 1

    if navigation_errors:
        print("\nAUDITORIA INCONCLUSIVA: houve erro ao abrir uma ou mais páginas.")
        return 1

    print("\nAUDITORIA DE REDE OK: nenhuma requisição a host externo não permitido.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Abre o site em Chromium headless, observa a rede e falha "
            "se houver requisição automática para host não permitido."
        )
    )
    parser.add_argument(
        "--base-url",
        help=(
            "Audita uma URL já publicada. Se omitido, serve site/ "
            "automaticamente em 127.0.0.1."
        ),
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Audita todos os arquivos HTML de site/.",
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help=(
            "Audita somente a rota indicada. Pode ser repetido. "
            "Ex.: --path / --path /docs/"
        ),
    )
    parser.add_argument(
        "--allow-host",
        action="append",
        default=[],
        help=(
            "Autoriza explicitamente outro host exato. "
            "Use somente quando a integração externa for intencional."
        ),
    )
    parser.add_argument(
        "--allow-subdomains-of",
        action="append",
        default=[],
        metavar="DOMINIO",
        help=(
            "Autoriza o domínio e todos os subdomínios. "
            "Ex.: --allow-subdomains-of fleck.dev.br"
        ),
    )
    parser.add_argument(
        "--settle-ms",
        type=int,
        default=300,
        help="Espera após cada carregamento para capturar requisições tardias.",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=15000,
        help="Timeout de navegação por página.",
    )
    parser.add_argument(
        "--report",
        default=str(DEFAULT_REPORT.relative_to(PROJECT_ROOT)),
        help="Arquivo JSON do relatório.",
    )
    return parser


def main() -> int:
    return audit(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
