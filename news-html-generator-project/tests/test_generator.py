import tempfile
import unittest
import zipfile
import json
from pathlib import Path
from unittest.mock import patch

from src.news_html_generator.generator import generate_html, generate_intranet_site
from src.news_html_generator.cli import main
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
        self.assertIn("Yonetici Ozeti", html)
        self.assertIn("Bu hafta one cikan gelismeler", html)
        self.assertIn("Habere Iliskin Kisa Degerlendirme", html)
        self.assertIn("Durum", html)
        self.assertIn("Yonetici Acisi", html)
        self.assertIn("Takip Basligi", html)

    def test_generates_single_merged_html_from_directory_with_advanced_filters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "inputs"
            input_dir.mkdir()

            build_docx(
                input_dir / "openai-briefing.docx",
                [
                    "OpenAI yeni ajan tabanli model ailesini tanitti ve kurumsal kullanim senaryolarini genisletti.",
                    "https://example.com/openai",
                ],
            )
            build_docx(
                input_dir / "anthropic-briefing.docx",
                [
                    "Anthropic servis surekliligi icin yeni altyapi ve guvenlik yatirimi planini paylasti.",
                    "https://example.com/anthropic",
                ],
            )
            build_docx(
                input_dir / "gemini-briefing.docx",
                [
                    "Gemini cok modlu arama ve dokuman ozetleme deneyimini yeni bir calisma alani ile birlestirdi.",
                    "https://example.com/gemini",
                ],
            )
            build_docx(
                input_dir / "alibaba-briefing.docx",
                [
                    "Alibaba yeni yapay zeka ve bulut is yuklerini destekleyen kurumsal platform guncellemesini duyurdu.",
                    "https://example.com/alibaba",
                ],
            )

            html = generate_html(input_dir, page_title="Birlesik Gündem")

        self.assertIn("<title>Birlesik Gündem</title>", html)
        self.assertIn("OpenAI yeni ajan tabanli model ailesini tanitti", html)
        self.assertIn("Anthropic servis surekliligi icin yeni altyapi", html)
        self.assertIn("filters-sidebar", html)
        self.assertIn('id="institution-filter"', html)
        self.assertIn('id="keyword-filter"', html)
        self.assertIn("OpenAI", html)
        self.assertIn("Anthropic", html)
        self.assertIn("Gemini", html)
        self.assertIn("Alibaba", html)
        self.assertIn('data-organization="OpenAI"', html)
        self.assertIn('data-organization="Gemini"', html)
        self.assertIn('data-organization="Alibaba"', html)
        self.assertIn('data-keywords="Yapay Zeka', html)
        self.assertIn("function applyFilters()", html)
        self.assertIn('id="theme-filter"', html)
        self.assertIn('id="document-filter"', html)
        self.assertIn('id="sort-order"', html)
        self.assertIn('id="active-filter-chips"', html)
        self.assertIn("Filtreleri Temizle", html)
        self.assertIn("layout-shell", html)
        self.assertIn("filters-scroll", html)
        self.assertIn("dashboard-overview", html)
        self.assertIn("dashboard-highlights", html)
        self.assertIn("function syncActiveFilterChips()", html)
        self.assertIn("function toggleCardExpansion(", html)
        self.assertIn("function sortCards()", html)
        self.assertIn("data-expanded=\"false\"", html)
        self.assertNotIn('id="exec-mode-toggle"', html)
        self.assertNotIn("Yonetici 5 Dakika", html)
        self.assertNotIn("exec-compact", html)
        self.assertIn("data-theme-filter", html)
        self.assertIn("data-source-filter", html)


class CliDispatchTests(unittest.TestCase):
    def test_directory_to_html_uses_merged_generation_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "inputs"
            input_dir.mkdir()
            output_html = Path(temp_dir) / "combined.html"

            with patch("src.news_html_generator.cli.generate_html", return_value="<html>merged</html>") as generate_html_mock:
                with patch("src.news_html_generator.cli.generate_intranet_site") as generate_site_mock:
                    with patch("sys.argv", ["prog", str(input_dir), str(output_html), "--title", "Toplu Bulten"]):
                        main()

            generate_html_mock.assert_called_once_with(input_dir, page_title="Toplu Bulten")
            generate_site_mock.assert_not_called()
            self.assertEqual(output_html.read_text(encoding="utf-8"), "<html>merged</html>")


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
        self.assertEqual(len(item.detail_sections), 3)
        self.assertEqual(item.detail_sections[0].title, "Durum")
        self.assertEqual(item.detail_sections[1].title, "Yonetici Acisi")
        self.assertEqual(item.detail_sections[2].title, "Takip Basligi")
        self.assertTrue(
            "Tedarik ve operasyon etkisi" in item.detail_sections[1].body
            or "Ticari yayginlasma ve altyapi etkisi" in item.detail_sections[1].body
        )


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


class PortalPortalUpgradesTests(unittest.TestCase):
    def test_multi_file_html_generation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_one = Path(temp_dir) / "one.docx"
            file_two = Path(temp_dir) / "two.docx"

            build_docx(
                file_one,
                [
                    "Türkiye savunma sanayisinde TUSAŞ yeni nesil insansız hava aracını uçurdu.",
                    "https://example.com/one",
                ],
            )
            build_docx(
                file_two,
                [
                    "Çin ve Asya borsaları yeni ekonomik teşvik paketi ile yükselişe geçti.",
                    "https://example.com/two",
                ],
            )

            html = generate_html([file_one, file_two], page_title="Portal Test")

            # Check title
            self.assertIn("<title>Portal Test</title>", html)

            # Check items
            self.assertIn("Türkiye savunma sanayisinde TUSAŞ", html)
            self.assertIn("Çin ve Asya borsaları yeni", html)

            # Check Region classifications in HTML
            self.assertIn('data-region="Türkiye"', html)
            self.assertIn('data-region="Asya"', html)

            # Check Category classifications in HTML
            self.assertIn('data-category="Askeri"', html)
            self.assertIn('data-category="Ekonomik"', html)

            # Check dropdown filters
            self.assertIn('id="region-filter"', html)
            self.assertIn('id="category-filter"', html)

            # Check TOC grouping structure
            self.assertIn('class="toc-region-group"', html)
            self.assertIn('class="toc-region-title"', html)

    def test_renders_portal_style_facet_filters_and_saved_views(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_one = Path(temp_dir) / "one.docx"
            file_two = Path(temp_dir) / "two.docx"
            file_three = Path(temp_dir) / "three.docx"

            build_docx(
                file_one,
                [
                    "Türkiye savunma sanayisinde TUSAŞ yeni nesil insansız hava aracını uçurdu.",
                    "https://example.com/one",
                ],
            )
            build_docx(
                file_two,
                [
                    "Çin ve Asya borsaları yeni ekonomik teşvik paketi ile yükselişe geçti.",
                    "https://example.com/two",
                ],
            )
            build_docx(
                file_three,
                [
                    "OpenAI kurumsal yapay zeka platformunu yeni güvenlik katmanlarıyla genişletti.",
                    "https://example.com/three",
                ],
            )

            html = generate_html([file_one, file_two, file_three], page_title="Portal Facet Test")

        self.assertIn('class="portal-rail"', html)
        self.assertIn('class="facet-section"', html)
        self.assertIn('class="facet-option"', html)
        self.assertIn('class="saved-view-list"', html)
        self.assertIn('data-view="operations"', html)
        self.assertIn('id="toolbar-query"', html)
        self.assertIn('id="facet-summary"', html)
        self.assertIn('class="content-layout"', html)
        self.assertIn('class="dashboard-card filters-sidebar"', html)
        self.assertNotIn('id="filter-drawer-toggle"', html)
        self.assertNotIn('class="filters-drawer"', html)
        self.assertNotIn('function toggleFilterDrawer()', html)
        self.assertNotIn('data-view="executive"', html)
        self.assertIn('data-collapsible="toc"', html)
        self.assertIn('function toggleDashboardSection(', html)
        self.assertIn('function applyPresetView(', html)
        self.assertIn('function toggleFacetOption(', html)
        self.assertNotIn("Kapsam Notu", html)
        self.assertIn('Türkiye (1)', html)
        self.assertIn('Asya (1)', html)
        self.assertIn('Teknolojik (1)', html)
        self.assertIn('Askeri (1)', html)


if __name__ == "__main__":
    unittest.main()
