"""Configura o repositório Git para usar os hooks versionados em ``.githooks``.

Este script atua na raiz do projeto, não dentro de ``site/``. O hook permanece
privado no repositório e executa os scripts de rebuild e validação antes do
commit.
"""

from __future__ import annotations

import subprocess

from site_utils import PROJECT_ROOT


HOOK = PROJECT_ROOT / ".githooks/pre-commit"


def main() -> int:
    """Torna o hook executável e configura ``core.hooksPath``."""

    if not HOOK.exists():
        raise SystemExit(
            f"Hook não encontrado: {HOOK.relative_to(PROJECT_ROOT)}"
        )

    # Preserva as permissões existentes e acrescenta os bits de execução.
    HOOK.chmod(HOOK.stat().st_mode | 0o111)

    subprocess.run(
        ["git", "config", "core.hooksPath", ".githooks"],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print(
        "Git configurado para usar .githooks/. "
        "O pre-commit executará rebuild e validação."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
