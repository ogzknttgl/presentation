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
class DetailSection:
    title: str
    body: str


@dataclass(slots=True)
class EnrichedNewsItem:
    body: str
    source_url: str
    closing: str
    source_document: str
    organization_name: str
    headline: str
    tags: list[str]
    theme_name: str
    summary_points: list[str]
    detail_sections: list[DetailSection]
    importance_score: int
    infographic_metrics: list[InfographicMetric]
    region: str = "Küresel"
    category: str = "Genel"


@dataclass(slots=True)
class EnrichedNewsletter:
    recipient: str
    items: list[EnrichedNewsItem]
    parse_strategy: str
    source_name: str
    warnings: list[str]
