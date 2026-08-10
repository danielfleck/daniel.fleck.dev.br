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


    def test_portfolio_cta_has_component_style(self) -> None:
        """O CTA 'Abrir conteúdo' precisa possuir estilo visual explícito."""

        components = (ROOT / "css/components.css").read_text(encoding="utf-8")
        portfolio = (ROOT / "portfolio/index.html").read_text(encoding="utf-8")

        self.assertIn(".project-link", components)
        self.assertIn('class="project-link"', portfolio)

    def test_assets_are_cache_busted(self) -> None:
        """HTML público deve referenciar CSS/JS com hash de conteúdo."""

        import hashlib

        portfolio = (ROOT / "portfolio/index.html").read_text(encoding="utf-8")
        css = ROOT / "css/components.css"
        digest = hashlib.sha256(css.read_bytes()).hexdigest()[:12]

        self.assertIn(f"/css/components.css?v={digest}", portfolio)


if __name__ == "__main__":
    unittest.main()
