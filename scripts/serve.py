"""Inicia um servidor HTTP local para pré-visualização do site estático."""

from __future__ import annotations

import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"
PORT = 8000


def main() -> int:
    """Serve a raiz do projeto em ``http://127.0.0.1:8000/``."""

    # SimpleHTTPRequestHandler usa o diretório de trabalho como raiz quando
    # nenhum diretório é informado explicitamente.
    os.chdir(ROOT)

    print(f"Servidor local: http://{HOST}:{PORT}/  (Ctrl+C para encerrar)")
    server = ThreadingHTTPServer((HOST, PORT), SimpleHTTPRequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
