"""Ativa todos os hooks versionados em .githooks/."""

from __future__ import annotations

import subprocess
from site_utils import PROJECT_ROOT

HOOKS_DIR = PROJECT_ROOT / ".githooks"

def main() -> int:
    if not HOOKS_DIR.is_dir():
        raise SystemExit("Pasta .githooks não encontrada.")

    hooks = [p for p in sorted(HOOKS_DIR.iterdir()) if p.is_file() and not p.name.startswith(".")]
    if not hooks:
        raise SystemExit("Nenhum hook encontrado.")

    for hook in hooks:
        hook.chmod(hook.stat().st_mode | 0o111)

    subprocess.run(
        ["git", "config", "core.hooksPath", ".githooks"],
        cwd=PROJECT_ROOT,
        check=True,
    )
    print("Hooks ativos:", ", ".join(p.name for p in hooks))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
