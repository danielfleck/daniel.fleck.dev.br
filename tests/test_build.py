"""Testes de integração para rebuild e validação do site."""

from __future__ import annotations

import subprocess
import sys
import unittest

from scripts.site_utils import ROOT


class BuildTests(unittest.TestCase):
    """Confirma que o repositório permanece reconstruído e válido."""

    def test_rebuild_is_idempotent(self) -> None:
        """O rebuild em modo check não deve detectar diferenças."""

        process = subprocess.run(
            [sys.executable, str(ROOT / "scripts/rebuild.py"), "--check"],
            cwd=ROOT,
        )
        self.assertEqual(process.returncode, 0)

    def test_validate(self) -> None:
        """O validador completo deve encerrar com código zero."""

        process = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate.py")],
            cwd=ROOT,
        )
        self.assertEqual(process.returncode, 0)


if __name__ == "__main__":
    unittest.main()
