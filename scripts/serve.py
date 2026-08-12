"""Inicia um servidor HTTP local para pré-visualização de ``site/``.

O comando deve ser executado a partir da raiz do repositório:

    python scripts/serve.py

Embora o script esteja fora da pasta pública, o servidor expõe somente
``site/`` como document root. Isso reproduz a nova organização planejada para
a hospedagem e evita disponibilizar scripts, templates, testes ou arquivos da
raiz do projeto durante a pré-visualização local.
"""

from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from site_utils import SITE_ROOT


HOST = "127.0.0.1"
PORT = 8000


def main() -> int:
    """Serve ``SITE_ROOT`` em ``http://127.0.0.1:8000/``."""

    if not SITE_ROOT.is_dir():
        raise SystemExit(f"Pasta pública não encontrada: {SITE_ROOT}")

    # O parâmetro directory evita alterar o cwd global do processo e garante
    # explicitamente que apenas site/ seja exposto pelo servidor local.
    def handler(*args, **kwargs):
        return SimpleHTTPRequestHandler(*args, directory=str(SITE_ROOT), **kwargs)

    print(f"Raiz pública: {SITE_ROOT}")
    print(f"Servidor local: http://{HOST}:{PORT}/  (Ctrl+C para encerrar)")
    server = ThreadingHTTPServer((HOST, PORT), handler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
