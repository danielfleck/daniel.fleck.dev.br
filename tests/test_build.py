"""Testes de integração para rebuild e validação do site."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import unittest

from scripts.site_utils import PROJECT_ROOT, SITE_ROOT


class BuildTests(unittest.TestCase):
    """Confirma que o repositório permanece reconstruído e válido."""

    def test_rebuild_is_idempotent(self) -> None:
        """O rebuild em modo check não deve detectar diferenças."""

        process = subprocess.run(
            [
                sys.executable,
                str(PROJECT_ROOT / "scripts/rebuild.py"),
                "--check",
            ],
            cwd=PROJECT_ROOT,
        )
        self.assertEqual(process.returncode, 0)

    def test_validate(self) -> None:
        """O validador completo deve encerrar com código zero."""

        process = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/validate.py")],
            cwd=PROJECT_ROOT,
        )
        self.assertEqual(process.returncode, 0)

    def test_portfolio_cta_has_component_style(self) -> None:
        """O CTA 'Abrir conteúdo' precisa possuir estilo visual explícito."""

        components = (SITE_ROOT / "css/components.css").read_text(
            encoding="utf-8"
        )
        portfolio = (SITE_ROOT / "portfolio/index.html").read_text(
            encoding="utf-8"
        )

        self.assertIn(".project-link", components)
        self.assertIn('class="project-link"', portfolio)

    def test_assets_are_cache_busted(self) -> None:
        """HTML público deve referenciar CSS/JS com hash de conteúdo."""

        portfolio = (SITE_ROOT / "portfolio/index.html").read_text(
            encoding="utf-8"
        )
        css = SITE_ROOT / "css/components.css"
        digest = hashlib.sha256(css.read_bytes()).hexdigest()[:12]

        self.assertIn(f"/css/components.css?v={digest}", portfolio)

    def test_public_site_is_isolated_in_site_directory(self) -> None:
        """A raiz pública deve ser ``site/`` e conter a página inicial."""

        self.assertTrue(SITE_ROOT.is_dir())
        self.assertTrue((SITE_ROOT / "index.html").is_file())
        self.assertFalse((PROJECT_ROOT / "index.html").exists())


    def test_mkdocs_source_is_outside_public_root(self) -> None:
        """Fontes MkDocs devem ficar fora de ``site/`` e build em site/docs."""

        source = PROJECT_ROOT / "mkdocs" / "docs"
        config = PROJECT_ROOT / "mkdocs" / "mkdocs.yml"
        output = SITE_ROOT / "docs"

        self.assertTrue(source.is_dir())
        self.assertTrue(config.is_file())
        self.assertTrue(output.is_dir())
        self.assertTrue((output / "index.html").is_file())

    def test_mkdocs_build_is_current(self) -> None:
        """O build MkDocs versionado deve corresponder aos fontes atuais."""

        process = subprocess.run(
            [
                sys.executable,
                str(PROJECT_ROOT / "scripts/build_docs.py"),
                "--check",
            ],
            cwd=PROJECT_ROOT,
        )
        self.assertEqual(process.returncode, 0)


if __name__ == "__main__":
    unittest.main()
