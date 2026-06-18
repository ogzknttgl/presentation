from __future__ import annotations

import json
import re
from pathlib import Path

from .enrichment import enrich_newsletter
from .parser import parse_docx_newsletter
from .renderer import render_newsletter_html
from .site_renderer import render_site_index


def generate_html(docx_path: str | Path, page_title: str = "Gunluk Haber Brifingi") -> str:
    newsletter = parse_docx_newsletter(docx_path)
    enriched_newsletter = enrich_newsletter(newsletter)
    return render_newsletter_html(enriched_newsletter, page_title=page_title)


def generate_intranet_site(
    input_path: str | Path,
    output_dir: str | Path,
    site_title: str = "Intranet Haber Merkezi",
) -> dict[str, object]:
    source_path = Path(input_path)
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    docx_files = [source_path] if source_path.is_file() else sorted(source_path.glob("*.docx"))
    if not docx_files:
        raise ValueError("No .docx files were found for intranet site generation.")

    entries: list[dict[str, object]] = []

    for docx_file in docx_files:
        newsletter = parse_docx_newsletter(docx_file)
        enriched_newsletter = enrich_newsletter(newsletter)
        page_title = _display_title(docx_file)
        output_name = f"{_slugify(docx_file.stem)}.html"
        html = render_newsletter_html(enriched_newsletter, page_title=page_title)
        (target_dir / output_name).write_text(html, encoding="utf-8")

        entries.append(
            {
                "title": page_title,
                "source_file": docx_file.name,
                "output_file": output_name,
                "item_count": len(enriched_newsletter.items),
                "parse_strategy": enriched_newsletter.parse_strategy,
                "warnings": enriched_newsletter.warnings,
                "themes": sorted({item.theme_name for item in enriched_newsletter.items}),
                "average_importance": round(
                    sum(item.importance_score for item in enriched_newsletter.items)
                    / max(len(enriched_newsletter.items), 1)
                ),
            }
        )

    index_html = render_site_index(site_title, entries)
    (target_dir / "index.html").write_text(index_html, encoding="utf-8")
    (target_dir / "manifest.json").write_text(
        json.dumps({"site_title": site_title, "entries": entries}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return {"entry_count": len(entries), "index_file": str(target_dir / "index.html"), "entries": entries}


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "newsletter"


def _display_title(docx_file: Path) -> str:
    return docx_file.stem.replace("-", " ").replace("_", " ").title()
