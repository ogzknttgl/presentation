from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from .models import NewsItem, Newsletter


WORD_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
URL_PATTERN = re.compile(r"^https?://\S+$")
CLOSING_PATTERNS = ("arz ederim", "bilgilerinize arz ederim", "saygilarimla")


def parse_docx_newsletter(docx_path: str | Path) -> Newsletter:
    source_path = Path(docx_path)
    paragraphs = _read_docx_paragraphs(source_path)
    meaningful_lines = [line.strip() for line in paragraphs if line.strip()]

    if not meaningful_lines:
        raise ValueError("Document does not contain any readable paragraphs.")

    recipient = _detect_recipient(meaningful_lines)
    warnings: list[str] = []
    items: list[NewsItem] = []
    buffer: list[str] = []
    last_item_index: int | None = None

    for line in meaningful_lines:
        if recipient and line == recipient:
            buffer.clear()
            continue
        if _is_closing_line(line):
            if last_item_index is not None and not buffer:
                items[last_item_index].closing = line
            buffer.clear()
            continue
        if URL_PATTERN.match(line):
            body_lines = [entry for entry in buffer if entry]
            if body_lines:
                items.append(NewsItem(body="\n\n".join(body_lines), source_url=line))
                last_item_index = len(items) - 1
            else:
                warnings.append(f"Skipped a source URL without body: {line}")
            buffer.clear()
            continue
        buffer.append(line)

    if buffer:
        warnings.append("Ignored trailing text that did not end with a source URL.")

    if not items:
        raise ValueError("No news items were detected in the document.")

    return Newsletter(
        recipient=recipient,
        items=items,
        parse_strategy="recipient_link_blocks" if recipient else "link_delimited_blocks",
        source_name=source_path.stem,
        warnings=warnings,
    )


def _read_docx_paragraphs(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as archive:
        document_xml = archive.read("word/document.xml")

    root = ElementTree.fromstring(document_xml)
    paragraphs: list[str] = []

    for paragraph in root.findall(".//w:body/w:p", WORD_NAMESPACE):
        texts = [
            node.text or ""
            for node in paragraph.findall(".//w:t", WORD_NAMESPACE)
        ]
        paragraphs.append("".join(texts))

    return paragraphs


def _detect_recipient(lines: list[str]) -> str:
    first_line = lines[0].strip().lower()
    if first_line.startswith("sayın ") or first_line.startswith("sayin "):
        return lines[0].strip()
    return ""


def _is_closing_line(line: str) -> bool:
    normalized = line.strip().lower()
    return any(normalized.startswith(pattern) for pattern in CLOSING_PATTERNS)
