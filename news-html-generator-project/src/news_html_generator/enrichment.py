from __future__ import annotations

import re

from .models import (
    DetailSection,
    EnrichedNewsItem,
    EnrichedNewsletter,
    InfographicMetric,
    Newsletter,
)


KEYWORD_RULES = (
    ("Yapay Zeka", ("yapay zeka", "ai", "ajan", "model")),
    ("Robotik", ("robot", "robotik", "otomasyon", "endustriyel")),
    ("Diplomasi", ("g7", "zirve", "muttefik", "ortak", "ulusal guvenlik", "diplomatik")),
    ("Siber Guvenlik", ("siber", "guvenlik", "savunma", "erisim kisitlamalari")),
    ("Altyapi", ("kesinti", "erisim sorunu", "outage", "altyapi", "hizmet aksaması", "dayaniklilik")),
    ("Kurumsal Etki", ("kurumsal", "stratejik", "rekabet", "kritik rol")),
)

REGION_RULES = (
    ("Türkiye", ("türkiye", "turkey", "ankara", "istanbul", "türk", "tusaş", "aselsan", "baykar")),
    ("Asya", ("asya", "asia", "çin", "china", "japonya", "japan", "hindistan", "india", "kore")),
    ("Avrupa", ("avrupa", "europe", "almanya", "germany", "fransa", "france", "ingiltere", "uk", "londra", "paris", "berlin", "brüksel", "ab ")),
    ("ABD", ("abd", "usa", "amerika", "washington", "new york", "silikon vadisi", "pentagon", "beyaz saray", "openai", "anthropic", "nvidia", "microsoft", "google", "meta", "amazon")),
)

CATEGORY_RULES = (
    ("Siyasi", ("siyasi", "politika", "hükümet", "bakan", "başkan", "seçim", "diplomasi", "diplomatik", "zirve", "lider", "g7", "nato")),
    ("Ekonomik", ("ekonomi", "ekonomik", "finans", "dolar", "avro", "tl", "enflasyon", "borsa", "faiz", "yatırım", "ticaret", "şirket", "gelir", "hisse", "büyüme", "pazar", "satış", "maliyet", "para")),
    ("Askeri", ("askeri", "savunma", "ordu", "silah", "savaş", "harekat", "mühimmat", "füze", "tusaş", "aselsan", "baykar", "pentagon")),
    ("Teknolojik", ("teknoloji", "teknolojik", "yazılım", "donanım", "yapay zeka", "ai", "veri", "siber", "robot", "bulut", "dijital", "model", "kod", "çip")),
)

THEME_RULES = (
    ("Otomasyon ve Robotik", ("robot", "robotik", "otomasyon", "endustriyel")),
    ("Jeopolitik ve Guvenlik", ("g7", "muttefik", "ulusal guvenlik", "diplomatik", "siber")),
    ("Servis Surekliligi", ("kesinti", "outage", "altyapi", "dayaniklilik", "erisim sorunu")),
    ("Kurumsal Donusum", ("rekabet", "kurumsal", "stratejik", "ajan", "model")),
)

METRIC_RULES = (
    ("Operasyon", ("otomasyon", "robot", "endustriyel", "altyapi", "servis")),
    ("Strateji", ("rekabet", "stratejik", "g7", "muttefik", "guvenlik")),
    ("Erisim", ("erisim", "kesinti", "yaygin", "kuresel", "platform")),
)

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
ORGANIZATION_LABELS = {
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "nvidia": "NVIDIA",
    "microsoft": "Microsoft",
    "google": "Google",
    "gemini": "Gemini",
    "meta": "Meta",
    "amazon": "Amazon",
    "alibaba": "Alibaba",
}


def enrich_newsletter(newsletter: Newsletter) -> EnrichedNewsletter:
    organization_name = _organization_name(newsletter.source_name, newsletter.items)
    return EnrichedNewsletter(
        recipient=newsletter.recipient,
        items=[
            _enrich_item(
                item.body,
                item.source_url,
                item.closing,
                source_document=newsletter.source_name,
                organization_name=organization_name,
            )
            for item in newsletter.items
        ],
        parse_strategy=newsletter.parse_strategy,
        source_name=newsletter.source_name,
        warnings=list(newsletter.warnings),
    )


def _detect_region(normalized: str) -> str:
    scores = {region: sum(normalized.count(kw) for kw in keywords) for region, keywords in REGION_RULES}
    max_region = max(scores, key=scores.get)
    if scores[max_region] > 0:
        return max_region
    return "Küresel"


def _detect_category(normalized: str) -> str:
    scores = {cat: sum(normalized.count(kw) for kw in keywords) for cat, keywords in CATEGORY_RULES}
    max_cat = max(scores, key=scores.get)
    if scores[max_cat] > 0:
        return max_cat
    return "Genel"


def _enrich_item(
    body: str,
    source_url: str,
    closing: str,
    *,
    source_document: str,
    organization_name: str,
) -> EnrichedNewsItem:
    normalized = _normalize(body)
    tags = [label for label, keywords in KEYWORD_RULES if any(keyword in normalized for keyword in keywords)]
    if not tags:
        tags = ["Genel Gundem"]

    theme_name = _pick_theme(normalized)
    summary_points = _summary_points(body)
    detail_sections = _detail_sections(body, tags, theme_name, source_document, organization_name)
    importance_score = _importance_score(tags, normalized)
    infographic_metrics = _build_metrics(normalized, importance_score)
    region = _detect_region(normalized)
    category = _detect_category(normalized)

    return EnrichedNewsItem(
        body=body,
        source_url=source_url,
        closing=closing,
        source_document=source_document,
        organization_name=organization_name,
        headline=_headline(body),
        tags=tags,
        theme_name=theme_name,
        summary_points=summary_points,
        detail_sections=detail_sections,
        importance_score=importance_score,
        infographic_metrics=infographic_metrics,
        region=region,
        category=category,
    )


def _pick_theme(normalized: str) -> str:
    for theme_name, keywords in THEME_RULES:
        if any(keyword in normalized for keyword in keywords):
            return theme_name
    return "Teknoloji Guncellemesi"


def _summary_points(body: str) -> list[str]:
    sentences = [sentence.strip() for sentence in SENTENCE_SPLIT_RE.split(body.strip()) if sentence.strip()]
    return sentences[:2] or [body.strip()]


def _importance_score(tags: list[str], normalized: str) -> int:
    score = 36 + len(tags) * 10
    if any(keyword in normalized for keyword in ("kritik", "kuresel", "ulusal guvenlik", "rekabet", "kesinti")):
        score += 16
    if any(keyword in normalized for keyword in ("robot", "yapay zeka", "ajan", "otomasyon")):
        score += 8
    return min(score, 96)


def _build_metrics(normalized: str, importance_score: int) -> list[InfographicMetric]:
    metrics: list[InfographicMetric] = []
    for label, keywords in METRIC_RULES:
        hits = sum(1 for keyword in keywords if keyword in normalized)
        value = min(30 + hits * 18 + importance_score // 5, 96)
        metrics.append(InfographicMetric(label=label, value=value))
    return metrics


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _headline(body: str) -> str:
    first_line = body.split("\n", 1)[0].strip()
    if len(first_line) <= 84:
        return first_line
    return f"{first_line[:81].rstrip()}..."


def _detail_sections(
    body: str,
    tags: list[str],
    theme_name: str,
    source_document: str,
    organization_name: str,
) -> list[DetailSection]:
    summary = _summary_points(body)[0]
    tag_text = ", ".join(tags[:3]) if tags else "Genel Gundem"
    document_label = source_document.replace("-", " ").replace("_", " ").title()
    institution_frame = _institution_frame(organization_name)

    return [
        DetailSection(
            title="Durum",
            body=summary,
        ),
        DetailSection(
            title="Yonetici Acisi",
            body=f"{institution_frame} Haber {organization_name} ekseninde {theme_name.lower()} basligina oturuyor; izleme etiketleri: {tag_text}.",
        ),
        DetailSection(
            title="Takip Basligi",
            body=f"Bu kayit {document_label} icinden geldi. Devam haberlerinde ayni kurum, tema ve kaynak akisinin surup surmedigi izlenmeli.",
        ),
    ]


def _organization_name(source_name: str, items: list) -> str:
    source_tokens = _normalize(source_name).replace("-", " ").replace("_", " ")
    for keyword, label in ORGANIZATION_LABELS.items():
        if keyword in source_tokens:
            return label

    combined = " ".join(item.body for item in items)
    normalized = _normalize(combined)
    for keyword, label in ORGANIZATION_LABELS.items():
        if keyword in normalized:
            return label

    cleaned = source_name.replace("-", " ").replace("_", " ").strip()
    return cleaned.title() if cleaned else "Genel Kaynak"


def _institution_frame(organization_name: str) -> str:
    normalized = _normalize(organization_name)
    if normalized in {"nvidia", "amd", "intel"}:
        return "Tedarik ve operasyon etkisi one cikiyor."
    if normalized in {"openai", "anthropic", "gemini", "google", "meta", "microsoft"}:
        return "Platform ve urun yol haritasi etkisi belirgin."
    if normalized in {"alibaba", "amazon"}:
        return "Ticari yayginlasma ve altyapi etkisi one cikiyor."
    return "Kurumsal izleme gereksinimi suruyor."
