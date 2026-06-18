import tempfile
import unittest
import zipfile
import json
from pathlib import Path

from src.news_html_generator.generator import generate_html, generate_intranet_site
from src.news_html_generator.enrichment import enrich_newsletter
from src.news_html_generator.parser import parse_docx_newsletter


DOCUMENT_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
{paragraphs}
    <w:sectPr />
  </w:body>
</w:document>
"""


def paragraph_xml(text: str) -> str:
    return f'    <w:p><w:r><w:t xml:space="preserve">{text}</w:t></w:r></w:p>\n'


def build_docx(path: Path, paragraphs: list[str]) -> None:
    document_xml = DOCUMENT_XML_TEMPLATE.format(
        paragraphs="".join(paragraph_xml(text) for text in paragraphs)
    )
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
"""
    relationships = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", relationships)
        archive.writestr("word/document.xml", document_xml)


class ParseDocxNewsletterTests(unittest.TestCase):
    def test_parses_multiple_news_items_from_docx(self) -> None:
        paragraphs = [
            "Sayın Başkanım,",
            "",
            "Alibaba robotlar için ilk yapay zekâ model ailesini tanıttı.",
            "https://example.com/alibaba",
            "",
            "Arz ederim.",
            "",
            "Sayın Başkanım,",
            "",
            "Anthropic erişim sorunları yaşadı.",
            "https://example.com/anthropic",
            "",
            "Arz ederim.",
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            docx_path = Path(temp_dir) / "newsletter.docx"
            build_docx(docx_path, paragraphs)

            newsletter = parse_docx_newsletter(docx_path)

        self.assertEqual(newsletter.recipient, "Sayın Başkanım,")
        self.assertEqual(len(newsletter.items), 2)
        self.assertEqual(
            newsletter.items[0].body,
            "Alibaba robotlar için ilk yapay zekâ model ailesini tanıttı.",
        )
        self.assertEqual(newsletter.items[0].source_url, "https://example.com/alibaba")
        self.assertEqual(newsletter.items[1].closing, "Arz ederim.")

    def test_joins_multiline_body_paragraphs(self) -> None:
        paragraphs = [
            "Sayın Başkanım,",
            "İlk paragraf.",
            "İkinci paragraf.",
            "https://example.com/story",
            "Arz ederim.",
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            docx_path = Path(temp_dir) / "newsletter.docx"
            build_docx(docx_path, paragraphs)

            newsletter = parse_docx_newsletter(docx_path)

        self.assertEqual(
            newsletter.items[0].body,
            "İlk paragraf.\n\nİkinci paragraf.",
        )

    def test_parses_link_delimited_documents_without_greeting_or_closing(self) -> None:
        paragraphs = [
            "Alibaba yeni ajan tabanli modelini tanitti.",
            "https://example.com/alibaba",
            "Anthropic servis surekliligini guclendirecek yeni altyapi planini acikladi.",
            "https://example.com/anthropic",
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            docx_path = Path(temp_dir) / "generic.docx"
            build_docx(docx_path, paragraphs)

            newsletter = parse_docx_newsletter(docx_path)

        self.assertEqual(newsletter.parse_strategy, "link_delimited_blocks")
        self.assertEqual(newsletter.recipient, "")
        self.assertEqual(len(newsletter.items), 2)
        self.assertEqual(newsletter.items[1].source_url, "https://example.com/anthropic")
        self.assertEqual(newsletter.items[0].body, "Alibaba yeni ajan tabanli modelini tanitti.")


class GenerateHtmlTests(unittest.TestCase):
    def test_generates_modern_html_from_parsed_newsletter(self) -> None:
        paragraphs = [
            "Sayın Başkanım,",
            "Alibaba robotlar için ilk yapay zekâ model ailesini tanıttı.",
            "https://example.com/alibaba",
            "Arz ederim.",
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            docx_path = Path(temp_dir) / "newsletter.docx"
            build_docx(docx_path, paragraphs)

            html = generate_html(docx_path, page_title="Gunluk Haber Brifingi")

        self.assertIn("<title>Gunluk Haber Brifingi</title>", html)
        self.assertIn('class="news-card"', html)
        self.assertIn("Alibaba robotlar için ilk yapay zekâ model ailesini tanıttı.", html)
        self.assertIn('href="https://example.com/alibaba"', html)
        self.assertNotIn("Sayın Başkanım,", html)
        self.assertNotIn("Arz ederim.", html)
        self.assertIn('class="insight-tags"', html)
        self.assertIn('class="infographic"', html)

    def test_renders_offline_friendly_controls_and_summary(self) -> None:
        paragraphs = [
            "Sayın Başkanım,",
            "Birinci haber.",
            "https://example.com/one",
            "Arz ederim.",
            "Sayın Başkanım,",
            "Ikinci haber.",
            "https://example.com/two",
            "Arz ederim.",
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            docx_path = Path(temp_dir) / "newsletter.docx"
            build_docx(docx_path, paragraphs)

            html = generate_html(docx_path, page_title="Aksam Ozeti")

        self.assertIn('class="toolbar"', html)
        self.assertIn('id="news-search"', html)
        self.assertIn("Toplam 2 haber", html)
        self.assertIn("Disa bagimli varlik kullanilmaz", html)
        self.assertIn("function filterCards()", html)
        self.assertIn("Icerik Indeksi", html)
        self.assertIn('class="dashboard"', html)
        self.assertIn('class="radar-card"', html)
        self.assertIn('href="#news-1"', html)
        self.assertIn("Tema Dagilimi", html)


class EnrichmentTests(unittest.TestCase):
    def test_enriches_items_with_keyword_tags_and_metrics(self) -> None:
        paragraphs = [
            "Sayın Başkanım,",
            "Alibaba robotlar için yeni yapay zeka model ailesini tanitti ve endustriyel otomasyon hedefini acikladi.",
            "https://example.com/alibaba",
            "Arz ederim.",
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            docx_path = Path(temp_dir) / "newsletter.docx"
            build_docx(docx_path, paragraphs)
            newsletter = parse_docx_newsletter(docx_path)

        enriched = enrich_newsletter(newsletter)
        item = enriched.items[0]

        self.assertIn("Yapay Zeka", item.tags)
        self.assertIn("Robotik", item.tags)
        self.assertEqual(item.theme_name, "Otomasyon ve Robotik")
        self.assertGreater(item.importance_score, 50)
        self.assertEqual(len(item.infographic_metrics), 3)
        self.assertEqual(item.summary_points[0], "Alibaba robotlar için yeni yapay zeka model ailesini tanitti ve endustriyel otomasyon hedefini acikladi.")


class IntranetSiteTests(unittest.TestCase):
    def test_generates_intranet_package_for_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "inputs"
            output_dir = Path(temp_dir) / "site"
            input_dir.mkdir()

            build_docx(
                input_dir / "briefing-one.docx",
                [
                    "Sayın Başkanım,",
                    "Alibaba robotik ve yapay zeka alaninda yeni bir hamle yapti.",
                    "https://example.com/alibaba",
                    "Arz ederim.",
                ],
            )
            build_docx(
                input_dir / "briefing-two.docx",
                [
                    "Anthropic servis kesintileri sonrasi altyapi yatirimlarini artiriyor.",
                    "https://example.com/anthropic",
                ],
            )

            package = generate_intranet_site(input_dir, output_dir, site_title="Intranet Haber Merkezi")

            index_html = (output_dir / "index.html").read_text(encoding="utf-8")
            manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
            first_exists = (output_dir / "briefing-one.html").exists()
            second_exists = (output_dir / "briefing-two.html").exists()

        self.assertEqual(package["entry_count"], 2)
        self.assertEqual(len(manifest["entries"]), 2)
        self.assertIn("Intranet Haber Merkezi", index_html)
        self.assertIn("briefing-one.html", index_html)
        self.assertIn("briefing-two.html", index_html)
        self.assertTrue(first_exists)
        self.assertTrue(second_exists)


if __name__ == "__main__":
    unittest.main()
