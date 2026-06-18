from __future__ import annotations

import argparse
from pathlib import Path

from .generator import generate_html, generate_intranet_site


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a modern HTML newsletter from a Word document."
    )
    parser.add_argument("input_docx", help="Path to the source .docx file")
    parser.add_argument("output_html", help="Path to the generated .html file")
    parser.add_argument(
        "--title",
        default="Gunluk Haber Brifingi",
        help="Page title used in the generated HTML output",
    )
    parser.add_argument(
        "--site-title",
        default="Intranet Haber Merkezi",
        help="Title used in the generated intranet index page for directory mode",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    input_path = Path(args.input_docx)
    output_path = Path(args.output_html)

    if input_path.is_dir() or output_path.suffix.lower() != ".html":
        generate_intranet_site(input_path, output_path, site_title=args.site_title)
        return

    html = generate_html(input_path, page_title=args.title)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
