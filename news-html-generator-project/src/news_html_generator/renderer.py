from __future__ import annotations

from collections import Counter
from html import escape
from urllib.parse import urlparse

from .models import EnrichedNewsletter, InfographicMetric


def render_newsletter_html(newsletter: EnrichedNewsletter, page_title: str) -> str:
    cards = "\n".join(
        _render_card(index=index, newsletter=newsletter)
        for index in range(len(newsletter.items))
    )
    safe_title = escape(page_title)
    news_count_label = f"Toplam {len(newsletter.items)} haber"
    dashboard_html = _render_dashboard(newsletter)

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <style>
    :root {{
      --bg: #efe7da;
      --ink: #142033;
      --muted: #5f6676;
      --line: rgba(20, 32, 51, 0.12);
      --card: rgba(255, 250, 244, 0.86);
      --card-strong: rgba(255, 255, 255, 0.94);
      --accent: #b45309;
      --accent-soft: #f59e0b;
      --support: #0f766e;
      --shadow: 0 28px 80px rgba(20, 32, 51, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", "Helvetica Neue", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(180, 83, 9, 0.20), transparent 24%),
        radial-gradient(circle at bottom right, rgba(15, 118, 110, 0.18), transparent 28%),
        linear-gradient(180deg, #f8f2e8 0%, #efe7da 100%);
    }}
    .shell {{
      width: min(1120px, calc(100% - 32px));
      margin: 40px auto 64px;
    }}
    .hero {{
      position: relative;
      overflow: hidden;
      padding: 38px;
      border: 1px solid var(--line);
      border-radius: 30px;
      background:
        linear-gradient(135deg, rgba(255,255,255,0.94), rgba(249,245,238,0.88));
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }}
    .hero::after {{
      content: "";
      position: absolute;
      inset: auto -60px -80px auto;
      width: 220px;
      height: 220px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(15,118,110,0.18), transparent 68%);
    }}
    .eyebrow {{
      margin: 0 0 12px;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      font-size: 0.76rem;
      color: var(--support);
      font-weight: 700;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(2.6rem, 6vw, 4.8rem);
      line-height: 0.92;
      max-width: 11ch;
      letter-spacing: -0.04em;
    }}
    .hero-layout {{
      display: grid;
      grid-template-columns: minmax(0, 1.5fr) minmax(300px, 0.9fr);
      gap: 24px;
      position: relative;
      z-index: 1;
    }}
    .hero-copy {{
      margin: 18px 0 0;
      max-width: 56ch;
      color: var(--muted);
      font-size: 1.04rem;
      line-height: 1.75;
    }}
    .summary-panel {{
      align-self: end;
      display: grid;
      gap: 12px;
      padding: 20px;
      border-radius: 22px;
      background: rgba(20, 32, 51, 0.92);
      color: #f8f5f0;
    }}
    .summary-kicker {{
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: rgba(248, 245, 240, 0.68);
    }}
    .summary-count {{
      font-size: 2rem;
      font-weight: 800;
      line-height: 1;
    }}
    .summary-note {{
      color: rgba(248, 245, 240, 0.76);
      line-height: 1.6;
      font-size: 0.95rem;
    }}
    .toolbar {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto auto;
      gap: 14px;
      align-items: center;
      margin-top: 22px;
      padding: 16px 18px;
      border: 1px solid var(--line);
      border-radius: 20px;
      background: var(--card-strong);
      box-shadow: 0 16px 40px rgba(20, 32, 51, 0.07);
    }}
    .search-input {{
      width: 100%;
      border: 1px solid rgba(20, 32, 51, 0.12);
      border-radius: 14px;
      padding: 14px 16px;
      font: inherit;
      color: var(--ink);
      background: #fffdfa;
    }}
    .search-input:focus {{
      outline: 2px solid rgba(180, 83, 9, 0.18);
      border-color: rgba(180, 83, 9, 0.32);
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 12px 16px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(180, 83, 9, 0.08);
      color: var(--accent);
      font-weight: 700;
      white-space: nowrap;
    }}
    .button {{
      border: 0;
      border-radius: 14px;
      padding: 13px 16px;
      font: inherit;
      font-weight: 700;
      color: #fffdf9;
      background: linear-gradient(135deg, var(--accent), var(--accent-soft));
      cursor: pointer;
    }}
    .dashboard {{
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr);
      gap: 22px;
      margin-top: 26px;
    }}
    .dashboard-card {{
      padding: 22px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--card-strong);
      box-shadow: 0 18px 50px rgba(20, 32, 51, 0.08);
    }}
    .dashboard-title {{
      margin: 0 0 14px;
      font-size: 1rem;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--muted);
    }}
    .toc-list {{
      display: grid;
      gap: 10px;
    }}
    .toc-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 12px 14px;
      border-radius: 16px;
      background: rgba(20, 32, 51, 0.05);
      text-decoration: none;
      color: var(--ink);
    }}
    .toc-item strong {{
      font-size: 0.94rem;
    }}
    .toc-theme {{
      color: var(--muted);
      font-size: 0.82rem;
    }}
    .dashboard-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 22px;
    }}
    .radar-card {{
      position: relative;
      overflow: hidden;
    }}
    .radial-stat {{
      display: grid;
      grid-template-columns: 128px minmax(0, 1fr);
      gap: 18px;
      align-items: center;
    }}
    .radial-ring {{
      --value: 0;
      width: 128px;
      aspect-ratio: 1;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background:
        radial-gradient(closest-side, #fffdf9 70%, transparent 72% 100%),
        conic-gradient(var(--support) calc(var(--value) * 1%), rgba(20, 32, 51, 0.08) 0);
      box-shadow: inset 0 0 0 1px rgba(20, 32, 51, 0.06);
    }}
    .radial-ring span {{
      font-size: 1.6rem;
      font-weight: 800;
    }}
    .radial-copy {{
      color: var(--muted);
      line-height: 1.65;
      font-size: 0.95rem;
    }}
    .distribution-list {{
      display: grid;
      gap: 12px;
      margin-top: 14px;
    }}
    .distribution-row {{
      display: grid;
      gap: 8px;
    }}
    .distribution-head {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      font-weight: 700;
    }}
    .distribution-track {{
      height: 10px;
      border-radius: 999px;
      background: rgba(20, 32, 51, 0.08);
      overflow: hidden;
    }}
    .distribution-fill {{
      height: 100%;
      border-radius: inherit;
      background: linear-gradient(90deg, var(--accent), var(--accent-soft));
    }}
    .source-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      font-size: 0.94rem;
    }}
    .source-table th,
    .source-table td {{
      text-align: left;
      padding: 10px 0;
      border-bottom: 1px solid rgba(20, 32, 51, 0.08);
    }}
    .stat-strip {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 14px;
    }}
    .mini-stat {{
      padding: 14px;
      border-radius: 18px;
      background: rgba(180, 83, 9, 0.08);
    }}
    .mini-stat strong {{
      display: block;
      font-size: 1.25rem;
      line-height: 1;
      margin-bottom: 6px;
    }}
    .mini-stat span {{
      color: var(--muted);
      font-size: 0.84rem;
    }}
    .grid {{
      display: grid;
      gap: 22px;
      margin-top: 28px;
    }}
    .news-card {{
      position: relative;
      overflow: hidden;
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--card);
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }}
    .news-card::before {{
      content: "";
      position: absolute;
      inset: 0 auto auto 0;
      width: 100%;
      height: 4px;
      background: linear-gradient(90deg, var(--accent), var(--support));
    }}
    .card-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .card-index {{
      display: inline-flex;
      width: 40px;
      height: 40px;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      background: #162033;
      color: #fff;
      font-size: 0.92rem;
      font-weight: 700;
    }}
    .source-host {{
      display: inline-flex;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(15, 118, 110, 0.10);
      color: var(--support);
      font-size: 0.86rem;
      font-weight: 700;
    }}
    .theme-badge {{
      display: inline-flex;
      margin-top: 14px;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(180, 83, 9, 0.10);
      color: var(--accent);
      font-size: 0.82rem;
      font-weight: 800;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .card-body {{
      margin: 18px 0 22px;
      color: var(--ink);
      font-size: 1.08rem;
      line-height: 1.84;
      white-space: pre-line;
    }}
    .insight-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.1fr) minmax(240px, 0.9fr);
      gap: 18px;
      margin-bottom: 22px;
    }}
    .insight-panel {{
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.58);
    }}
    .panel-title {{
      margin: 0 0 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 0.74rem;
      font-weight: 800;
    }}
    .insight-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 0;
      padding: 0;
      list-style: none;
    }}
    .insight-tags li {{
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(20, 32, 51, 0.08);
      color: var(--ink);
      font-size: 0.88rem;
      font-weight: 700;
    }}
    .summary-list {{
      margin: 0;
      padding-left: 18px;
      color: var(--ink);
      line-height: 1.6;
    }}
    .summary-list li + li {{
      margin-top: 8px;
    }}
    .infographic {{
      display: grid;
      gap: 12px;
    }}
    .score-chip {{
      display: inline-flex;
      width: fit-content;
      margin-bottom: 14px;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(15, 118, 110, 0.10);
      color: var(--support);
      font-weight: 800;
    }}
    .metric {{
      display: grid;
      gap: 8px;
    }}
    .metric-head {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      font-size: 0.9rem;
      font-weight: 700;
      color: var(--ink);
    }}
    .metric-track {{
      height: 10px;
      border-radius: 999px;
      background: rgba(20, 32, 51, 0.08);
      overflow: hidden;
    }}
    .metric-fill {{
      height: 100%;
      border-radius: inherit;
      background: linear-gradient(90deg, var(--support), var(--accent-soft));
    }}
    .card-footer {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      padding-top: 18px;
      border-top: 1px solid rgba(95, 108, 131, 0.16);
    }}
    .source-link {{
      color: var(--accent);
      font-weight: 700;
      text-decoration: none;
    }}
    .source-link:hover {{
      text-decoration: underline;
    }}
    .meta-note {{
      color: var(--muted);
      font-size: 0.92rem;
    }}
    @media (max-width: 720px) {{
      .shell {{
        width: min(100% - 20px, 1120px);
        margin-top: 20px;
      }}
      .hero, .news-card {{
        padding: 22px;
        border-radius: 22px;
      }}
      .hero-layout,
      .toolbar,
      .insight-grid {{
        grid-template-columns: 1fr;
      }}
      .card-footer {{
        align-items: flex-start;
      }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="hero-layout">
        <div>
          <p class="eyebrow">Günlük Haber Akışı</p>
          <h1>{safe_title}</h1>
          <p class="hero-copy">Word dokümanındaki haber metinleri korunarak, kapalı ağ içinde güvenle kullanılabilecek tek dosyalık bir HTML bültene dönüştürüldü.</p>
        </div>
        <aside class="summary-panel">
          <div class="summary-kicker">Bülten Özeti</div>
          <div class="summary-count">{news_count_label}</div>
          <div class="summary-note">Disa bagimli varlik kullanilmaz. Tum stil ve etkilesim ayni HTML dosyasina gomuludur.</div>
        </aside>
      </div>
    </section>
    <section class="toolbar">
      <input id="news-search" class="search-input" type="search" placeholder="Haber metni veya kaynak alan adina gore filtrele" oninput="filterCards()">
      <div class="chip">{news_count_label}</div>
      <button class="button" type="button" onclick="window.print()">Yazdir veya PDF Al</button>
    </section>
    {dashboard_html}
    <section class="grid">
      {cards}
    </section>
  </main>
  <script>
    function filterCards() {{
      const query = document.getElementById("news-search").value.toLowerCase().trim();
      const cards = Array.from(document.querySelectorAll(".news-card"));
      for (const card of cards) {{
        const haystack = (card.dataset.search || "").toLowerCase();
        card.hidden = query !== "" && !haystack.includes(query);
      }}
    }}
  </script>
</body>
</html>
"""


def _render_card(index: int, newsletter: EnrichedNewsletter) -> str:
    item = newsletter.items[index]
    safe_body = escape(item.body)
    safe_url = escape(item.source_url, quote=True)
    host_label = _source_host_label(item.source_url)
    search_text = escape(f"{item.body} {host_label}", quote=True)
    safe_host = escape(host_label)
    safe_theme = escape(item.theme_name)
    tags_html = "".join(f"<li>{escape(tag)}</li>" for tag in item.tags)
    summary_html = "".join(f"<li>{escape(point)}</li>" for point in item.summary_points)
    metrics_html = "".join(_render_metric(metric) for metric in item.infographic_metrics)

    return f"""<article id="news-{index + 1}" class="news-card" data-search="{search_text}">
  <div class="card-top">
    <div class="card-index">{index + 1:02d}</div>
    <div class="source-host">{safe_host}</div>
  </div>
  <div class="theme-badge">{safe_theme}</div>
  <div class="card-body">{safe_body}</div>
  <div class="insight-grid">
    <section class="insight-panel">
      <p class="panel-title">Anahtar Etiketler</p>
      <ul class="insight-tags">{tags_html}</ul>
    </section>
    <section class="insight-panel">
      <div class="infographic">
        <div class="score-chip">Onem Skoru {item.importance_score}/100</div>
        {metrics_html}
      </div>
    </section>
  </div>
  <section class="insight-panel">
    <p class="panel-title">One Cikanlar</p>
    <ul class="summary-list">{summary_html}</ul>
  </section>
  <footer class="card-footer">
    <a class="source-link" href="{safe_url}" target="_blank" rel="noopener noreferrer">Kaynağı Aç</a>
    <span class="meta-note">Kapali ag uyumlu tek dosya bulten gorunumu</span>
  </footer>
</article>"""


def _source_host_label(source_url: str) -> str:
    host = urlparse(source_url).netloc.lower()
    return host.removeprefix("www.") or "kaynak"


def _render_metric(metric: InfographicMetric) -> str:
    safe_label = escape(metric.label)
    return f"""<div class="metric">
  <div class="metric-head">
    <span>{safe_label}</span>
    <span>{metric.value}</span>
  </div>
  <div class="metric-track">
    <div class="metric-fill" style="width: {metric.value}%"></div>
  </div>
</div>"""


def _render_dashboard(newsletter: EnrichedNewsletter) -> str:
    toc_html = "".join(_render_toc_item(index, item.theme_name) for index, item in enumerate(newsletter.items, start=1))
    avg_importance = round(sum(item.importance_score for item in newsletter.items) / max(len(newsletter.items), 1))
    theme_counts = Counter(item.theme_name for item in newsletter.items)
    source_counts = Counter(_source_host_label(item.source_url) for item in newsletter.items)
    total_items = max(len(newsletter.items), 1)

    theme_distribution = "".join(
        _render_distribution_row(theme, count, total_items) for theme, count in theme_counts.most_common()
    )
    source_rows = "".join(
        f"<tr><td>{escape(host)}</td><td>{count}</td><td>%{round(count / total_items * 100)}</td></tr>"
        for host, count in source_counts.most_common()
    )

    top_tag_count = len({tag for item in newsletter.items for tag in item.tags})
    avg_metrics = [metric.value for item in newsletter.items for metric in item.infographic_metrics]
    heat_index = round(sum(avg_metrics) / max(len(avg_metrics), 1))

    return f"""<section class="dashboard">
  <aside class="dashboard-card">
    <h2 class="dashboard-title">Icerik Indeksi</h2>
    <div class="toc-list">{toc_html}</div>
  </aside>
  <div class="dashboard-grid">
    <section class="dashboard-card">
      <div class="radar-card">
        <h2 class="dashboard-title">Durum Gosterge Paneli</h2>
        <div class="radial-stat">
          <div class="radial-ring" style="--value: {avg_importance}">
            <span>{avg_importance}</span>
          </div>
          <div class="radial-copy">Ortalama onem skoru haberlerin kurumsal etkisini, operasyon yogunlugunu ve erisim boyutunu ozetler.</div>
        </div>
        <div class="stat-strip">
          <div class="mini-stat"><strong>{len(newsletter.items)}</strong><span>Toplam Kayit</span></div>
          <div class="mini-stat"><strong>{top_tag_count}</strong><span>Aktif Etiket</span></div>
          <div class="mini-stat"><strong>{heat_index}</strong><span>Gundem Indeksi</span></div>
        </div>
      </div>
    </section>
    <section class="dashboard-card">
      <h2 class="dashboard-title">Tema Dagilimi</h2>
      <div class="distribution-list">{theme_distribution}</div>
    </section>
    <section class="dashboard-card">
      <h2 class="dashboard-title">Kaynak Yogunlugu</h2>
      <table class="source-table">
        <thead><tr><th>Kaynak</th><th>Adet</th><th>Pay</th></tr></thead>
        <tbody>{source_rows}</tbody>
      </table>
    </section>
    <section class="dashboard-card">
      <h2 class="dashboard-title">Kapsam Notu</h2>
      <div class="radial-copy">Bu sayfa tamamen kapali ag icin uretilir. Chartlar, yuzdeler, indeksler ve navigasyon HTML icine gomulu hesaplamalardan beslenir.</div>
    </section>
  </div>
</section>"""


def _render_toc_item(index: int, theme_name: str) -> str:
    return f"""<a class="toc-item" href="#news-{index}">
  <div>
    <strong>Haber {index:02d}</strong>
    <div class="toc-theme">{escape(theme_name)}</div>
  </div>
  <span>Git</span>
</a>"""


def _render_distribution_row(label: str, count: int, total_items: int) -> str:
    percentage = round(count / total_items * 100)
    return f"""<div class="distribution-row">
  <div class="distribution-head">
    <span>{escape(label)}</span>
    <span>%{percentage}</span>
  </div>
  <div class="distribution-track">
    <div class="distribution-fill" style="width: {percentage}%"></div>
  </div>
</div>"""
