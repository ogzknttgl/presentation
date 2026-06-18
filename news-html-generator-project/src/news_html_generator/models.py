from dataclasses import dataclass, field


@dataclass(slots=True)
class NewsItem:
    body: str
    source_url: str
    closing: str = ""


@dataclass(slots=True)
class Newsletter:
    items: list[NewsItem]
    recipient: str = ""
    parse_strategy: str = ""
    source_name: str = ""
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InfographicMetric:
    label: str
    value: int


@dataclass(slots=True)
class EnrichedNewsItem:
    body: str
    source_url: str
    closing: str
    headline: str
    tags: list[str]
    theme_name: str
    summary_points: list[str]
    importance_score: int
    infographic_metrics: list[InfographicMetric]


@dataclass(slots=True)
class EnrichedNewsletter:
    recipient: str
    items: list[EnrichedNewsItem]
    parse_strategy: str
    source_name: str
    warnings: list[str]
