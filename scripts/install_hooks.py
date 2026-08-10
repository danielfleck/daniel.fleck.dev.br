"""Configura o repositório Git para usar os hooks versionados em ``.githooks``.

O Git não compartilha a configuração ``core.hooksPath`` pelo próprio clone.
Por isso, este script deve ser executado uma vez em cada nova cópia local do
repositório.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".githooks/pre-commit"


def main() -> int:
    """Torna o hook executável e configura ``core.hooksPath``."""

    if not HOOK.exists():
        raise SystemExit(f"Hook não encontrado: {HOOK.relative_to(ROOT)}")

    # Preserva as permissões existentes e acrescenta os bits de execução.
    HOOK.chmod(HOOK.stat().st_mode | 0o111)

    subprocess.run(
        ["git", "config", "core.hooksPath", ".githooks"],
        cwd=ROOT,
        check=True,
    )

    print(
        "Git configurado para usar .githooks/. "
        "O pre-commit executará rebuild e validação."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
