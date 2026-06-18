from __future__ import annotations

import re

from .models import (
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


def enrich_newsletter(newsletter: Newsletter) -> EnrichedNewsletter:
    return EnrichedNewsletter(
        recipient=newsletter.recipient,
        items=[_enrich_item(item.body, item.source_url, item.closing) for item in newsletter.items],
        parse_strategy=newsletter.parse_strategy,
        source_name=newsletter.source_name,
        warnings=list(newsletter.warnings),
    )


def _enrich_item(body: str, source_url: str, closing: str) -> EnrichedNewsItem:
    normalized = _normalize(body)
    tags = [label for label, keywords in KEYWORD_RULES if any(keyword in normalized for keyword in keywords)]
    if not tags:
        tags = ["Genel Gundem"]

    theme_name = _pick_theme(normalized)
    summary_points = _summary_points(body)
    importance_score = _importance_score(tags, normalized)
    infographic_metrics = _build_metrics(normalized, importance_score)

    return EnrichedNewsItem(
        body=body,
        source_url=source_url,
        closing=closing,
        headline=_headline(body),
        tags=tags,
        theme_name=theme_name,
        summary_points=summary_points,
        importance_score=importance_score,
        infographic_metrics=infographic_metrics,
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
