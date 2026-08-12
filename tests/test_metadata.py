"""Testes das regras de metadados usadas para gerar o conteúdo estático."""

from __future__ import annotations

import unittest

from scripts.site_utils import SITE_ROOT, scan_content, tag_slug


class MetadataTests(unittest.TestCase):
    """Protege invariantes importantes dos blocos CONTENT-META."""

    def test_content_has_unique_keys(self) -> None:
        """Não pode existir o mesmo par tipo/slug mais de uma vez."""

        items = scan_content(SITE_ROOT)
        keys = [(item.type, item.slug) for item in items]
        self.assertEqual(len(keys), len(set(keys)))

    def test_content_required_fields(self) -> None:
        """Todo conteúdo precisa dos campos mínimos usados pelo build."""

        for item in scan_content(SITE_ROOT):
            self.assertTrue(item.title)
            self.assertTrue(item.summary)
            self.assertTrue(item.published)
            self.assertTrue(item.tags)

    def test_tag_slugs_do_not_collide(self) -> None:
        """Tags distintas não podem resultar na mesma URL normalizada."""

        seen: dict[str, str] = {}

        for item in scan_content(SITE_ROOT):
            for tag in item.tags:
                slug = tag_slug(tag)
                if slug in seen:
                    self.assertEqual(seen[slug], tag)
                seen[slug] = tag


if __name__ == "__main__":
    unittest.main()
