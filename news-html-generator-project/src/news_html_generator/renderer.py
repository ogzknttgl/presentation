from __future__ import annotations

from collections import Counter
from html import escape
from urllib.parse import urlparse

from .models import EnrichedNewsletter, InfographicMetric, EnrichedNewsItem


def render_newsletter_html(newsletter: EnrichedNewsletter, page_title: str) -> str:
    cards = "\n".join(
        _render_card(index=index, newsletter=newsletter)
        for index in range(len(newsletter.items))
    )
    safe_title = escape(page_title)
    news_count_label = f"Toplam {len(newsletter.items)} haber"
    dashboard_html = _render_dashboard(newsletter)
    filters_html = _render_filters(newsletter)

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
      --card: rgba(255, 250, 244, 0.90);
      --card-strong: rgba(255, 255, 255, 0.96);
      --accent: #b45309;
      --accent-soft: #f59e0b;
      --support: #0f766e;
      --shadow: 0 24px 72px rgba(20, 32, 51, 0.08);
    }}
    
    * {{ box-sizing: border-box; }}
    
    body {{
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", "Helvetica Neue", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(180, 83, 9, 0.12), transparent 28%),
        radial-gradient(circle at bottom right, rgba(15, 118, 110, 0.10), transparent 32%),
        linear-gradient(180deg, #f8f2e8 0%, #efe7da 100%);
      background-attachment: fixed;
      line-height: 1.6;
    }}
    
    .shell {{
      width: min(1440px, calc(100% - 48px));
      margin: 40px auto 80px;
    }}
    
    .layout-shell {{
      width: 100%;
    }}
    
    /* Clean Classic Header */
    .hero {{
      position: relative;
      overflow: hidden;
      padding: 40px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: linear-gradient(135deg, rgba(255,255,255,0.96), rgba(249,245,238,0.90));
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
      margin-bottom: 32px;
    }}
    
    .hero-layout {{
      display: grid;
      grid-template-columns: 1fr minmax(280px, auto);
      gap: 32px;
      align-items: center;
    }}
    
    .eyebrow {{
      margin: 0 0 10px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 0.78rem;
      color: var(--support);
      font-weight: 700;
    }}
    
    h1 {{
      margin: 0 0 16px;
      font-size: clamp(2.2rem, 5vw, 3.6rem);
      line-height: 1.05;
      letter-spacing: -0.03em;
      font-weight: 800;
    }}
    
    .hero-copy {{
      margin: 0;
      max-width: 60ch;
      color: var(--muted);
      font-size: 1.02rem;
      line-height: 1.7;
    }}
    
    .summary-panel {{
      padding: 24px;
      border-radius: 18px;
      background: var(--ink);
      color: #f8f5f0;
      box-shadow: 0 12px 32px rgba(20, 32, 51, 0.15);
    }}
    
    .summary-kicker {{
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: rgba(248, 245, 240, 0.6);
      margin-bottom: 4px;
      font-weight: 600;
    }}
    
    .summary-count {{
      font-size: 1.8rem;
      font-weight: 800;
      line-height: 1.2;
      margin-bottom: 6px;
    }}
    
    .summary-note {{
      color: rgba(248, 245, 240, 0.75);
      font-size: 0.85rem;
      line-height: 1.5;
    }}
    
    /* 2-Column Classic Layout */
    .content-layout {{
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr);
      gap: 24px;
      align-items: start;
    }}
    
    .filters-sidebar {{
      position: sticky;
      top: 24px;
      max-height: calc(100vh - 48px);
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 20px;
      background: var(--card-strong);
      box-shadow: var(--shadow);
    }}
    .portal-rail {{
      overflow: hidden;
    }}
    .filters-scroll {{
      padding: 24px;
      max-height: calc(100vh - 48px);
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
      overscroll-behavior: contain;
    }}
    .portal-kicker {{
      margin: 0 0 6px;
      font-size: 0.7rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--support);
    }}
    
    .dashboard-title {{
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--ink);
      margin: 0 0 8px;
      letter-spacing: -0.01em;
    }}
    
    .filter-help {{
      color: var(--muted);
      font-size: 0.85rem;
      line-height: 1.5;
    }}
    .facet-summary {{
      padding: 10px 14px;
      border-radius: 12px;
      background: rgba(20, 32, 51, 0.04);
      border: 1px solid rgba(20, 32, 51, 0.08);
      color: var(--ink);
      font-size: 0.82rem;
      line-height: 1.4;
    }}
    .saved-view-list {{
      display: grid;
      gap: 8px;
    }}
    .saved-view-button {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 11px 12px;
      background: rgba(20, 32, 51, 0.03);
      color: var(--ink);
      font: inherit;
      font-size: 0.84rem;
      font-weight: 700;
      text-align: left;
      cursor: pointer;
    }}
    .saved-view-button:hover,
    .saved-view-button[data-active="true"] {{
      background: rgba(180, 83, 9, 0.08);
      border-color: rgba(180, 83, 9, 0.25);
      color: var(--accent);
    }}
    
    .filter-stats {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 16px;
    }}
    
    .filter-stat {{
      background: rgba(20, 32, 51, 0.03);
      border: 1px solid var(--line);
      padding: 10px;
      border-radius: 12px;
      text-align: center;
    }}
    
    .filter-stat strong {{
      display: block;
      font-size: 1.25rem;
      color: var(--ink);
      font-weight: 800;
    }}
    
    .filter-stat span {{
      font-size: 0.7rem;
      color: var(--muted);
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.05em;
    }}
    
    .filters-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .facet-section {{
      display: grid;
      gap: 10px;
      padding-top: 14px;
      border-top: 1px solid rgba(20, 32, 51, 0.08);
    }}
    .facet-options {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .facet-option {{
      border: 1px solid rgba(20, 32, 51, 0.10);
      border-radius: 999px;
      padding: 8px 12px;
      background: #fff;
      color: var(--ink);
      font: inherit;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease;
    }}
    .facet-option:hover,
    .facet-option[data-active="true"] {{
      background: rgba(180, 83, 9, 0.09);
      border-color: rgba(180, 83, 9, 0.28);
      color: var(--accent);
    }}
    .filter-state-controls {{
      display: none;
    }}
    
    .filters-label {{
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--muted);
    }}
    
    .filter-select, .filter-input, .search-input, .toolbar-select {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 10px 12px;
      font-family: inherit;
      font-size: 0.88rem;
      color: var(--ink);
      background: #ffffff;
      outline: none;
    }}
    
    .filter-select:focus, .filter-input:focus, .search-input:focus, .toolbar-select:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(180, 83, 9, 0.1);
    }}
    
    .filter-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    
    .filter-pill {{
      border: 1px solid var(--line);
      border-radius: 20px;
      padding: 6px 12px;
      background: rgba(20, 32, 51, 0.04);
      color: var(--ink);
      font-family: inherit;
      font-size: 0.8rem;
      cursor: pointer;
    }}
    
    .filter-pill:hover {{
      background: rgba(180, 83, 9, 0.06);
      border-color: var(--accent);
      color: var(--accent);
    }}
    
    .filters-actions {{
      margin-top: 10px;
    }}
    
    /* Content Column */
    .content-stack {{
      display: flex;
      flex-direction: column;
      gap: 32px;
    }}
    .portal-commandbar {{
      display: grid;
      gap: 10px;
    }}
    
    .toolbar {{
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      padding: 16px 20px;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: var(--card-strong);
      box-shadow: var(--shadow);
    }}
    .commandbar-main,
    .commandbar-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }}
    .commandbar-actions {{
      justify-content: flex-end;
      flex-wrap: wrap;
      margin-left: auto;
    }}
    .toolbar-query-shell {{
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
      flex: 1;
    }}
    .toolbar-caption {{
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
      white-space: nowrap;
    }}
    
    .search-input {{
      padding: 11px 14px;
    }}
    
    .active-filter-chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: -12px;
    }}
    
    .active-chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 20px;
      border: 1px solid var(--line);
      background: var(--card-strong);
      color: var(--ink);
      font-size: 0.82rem;
      font-weight: 700;
      box-shadow: 0 2px 6px rgba(20, 32, 51, 0.02);
    }}
    
    .active-chip button {{
      border: 0;
      padding: 0;
      background: transparent;
      color: var(--accent);
      font-family: inherit;
      font-weight: 800;
      cursor: pointer;
    }}
    
    .button, .secondary-button {{
      font-family: inherit;
      font-weight: 700;
      font-size: 0.88rem;
      padding: 11px 18px;
      border-radius: 12px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }}
    
    .button {{
      border: 0;
      color: #ffffff;
      background: linear-gradient(135deg, var(--accent), var(--accent-soft));
    }}
    
    .button:hover {{
      opacity: 0.95;
    }}
    
    .secondary-button {{
      border: 1px solid var(--line);
      color: var(--ink);
      background: rgba(20, 32, 51, 0.03);
    }}
    
    .secondary-button:hover {{
      background: rgba(20, 32, 51, 0.06);
    }}
    
    .chip {{
      padding: 10px 14px;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: var(--card);
      color: var(--accent);
      font-weight: 700;
      font-size: 0.85rem;
    }}
    
    /* Overview Dashboard section */
    .dashboard {{
      display: flex;
      flex-direction: column;
      gap: 32px;
    }}
    
    .dashboard-overview {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }}
    
    .overview-stat {{
      background: var(--card);
      border: 1px solid var(--line);
      padding: 20px;
      border-radius: 16px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(8px);
    }}
    
    .overview-label {{
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--muted);
      margin: 0 0 6px;
      letter-spacing: 0.05em;
    }}
    
    .overview-value {{
      font-size: 1.7rem;
      font-weight: 800;
      color: var(--ink);
      line-height: 1.2;
      margin-bottom: 4px;
    }}
    
    .overview-note {{
      font-size: 0.78rem;
      color: var(--muted);
    }}
    
    .executive-summary {{
      background: var(--card-strong);
      border: 1px solid var(--line);
      padding: 28px;
      border-radius: 20px;
      box-shadow: var(--shadow);
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 32px;
    }}
    
    .executive-copy {{
      color: var(--muted);
      font-size: 0.98rem;
      line-height: 1.7;
      margin: 0;
    }}
    
    .executive-list {{
      margin: 0;
      padding-left: 20px;
      color: var(--muted);
      font-size: 0.95rem;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    
    /* Highlights area containing TOC and Stats */
    .dashboard-highlights {{
      display: grid;
      grid-template-columns: minmax(0, 1.12fr) minmax(320px, 0.88fr);
      gap: 24px;
    }}
    
    .dashboard-primary {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    
    .dashboard-secondary {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    
    .dashboard-card.compact {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 20px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(8px);
    }}
    .dashboard-card-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 12px;
    }}
    .dashboard-card-head .dashboard-title {{
      margin: 0;
    }}
    .dashboard-toggle {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 8px 12px;
      background: rgba(20, 32, 51, 0.04);
      color: var(--ink);
      font: inherit;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
    }}
    .collapsible-panel[hidden] {{
      display: none;
    }}
    
    /* Table of Contents Grouped by Region */
    .toc-list {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      max-height: 520px;
      overflow: auto;
      padding-right: 4px;
    }}
    
    .toc-region-group {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    
    .toc-region-title {{
      font-size: 0.8rem;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--muted);
      letter-spacing: 0.05em;
      border-bottom: 1px solid var(--line);
      padding-bottom: 6px;
      margin-bottom: 4px;
    }}
    
    .toc-region-items {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    
    .toc-item {{
      text-decoration: none;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 12px;
      border-radius: 10px;
      background: rgba(255,255,255,0.4);
      border: 1px solid transparent;
      transition: background 0.2s, border-color 0.2s;
    }}
    
    .toc-item:hover {{
      background: var(--card-strong);
      border-color: var(--line);
    }}
    
    .toc-item-headline {{
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--ink);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 320px;
    }}
    
    .toc-item-meta {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.78rem;
      color: var(--muted);
    }}
    
    .toc-org {{
      font-weight: 700;
      color: var(--support);
    }}
    
    .toc-cat {{
      font-weight: 600;
      color: var(--accent);
      background: rgba(180, 83, 9, 0.06);
      padding: 2px 6px;
      border-radius: 6px;
      font-size: 0.72rem;
      text-transform: uppercase;
    }}
    
    /* Gündem Nabzı */
    .radial-stat {{
      display: flex;
      align-items: center;
      gap: 20px;
      margin: 16px 0;
    }}
    
    .radial-ring {{
      position: relative;
      width: 72px;
      height: 72px;
      border-radius: 50%;
      background: conic-gradient(var(--support) calc(var(--value) * 1%), var(--line) 0);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    
    .radial-ring::after {{
      content: "";
      position: absolute;
      width: 58px;
      height: 58px;
      border-radius: 50%;
      background: #fffdfa;
    }}
    
    .radial-ring span {{
      position: relative;
      z-index: 1;
      font-size: 1.3rem;
      font-weight: 800;
      color: var(--ink);
    }}
    
    .radial-copy {{
      font-size: 0.88rem;
      color: var(--muted);
      line-height: 1.5;
    }}
    
    .stat-strip {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      border-top: 1px solid var(--line);
      padding-top: 16px;
      margin-top: 12px;
    }}
    
    .mini-stat {{
      text-align: center;
      display: flex;
      flex-direction: column;
    }}
    
    .mini-stat strong {{ font-size: 1.1rem; font-weight: 800; color: var(--ink); }}
    .mini-stat span {{ font-size: 0.68rem; color: var(--muted); text-transform: uppercase; font-weight: 700; }}
    
    .distribution-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    
    .distribution-row {{
      width: 100%;
    }}
    
    .distribution-button {{
      background: none;
      border: none;
      width: 100%;
      padding: 0;
      cursor: pointer;
      display: block;
      text-align: left;
      color: inherit;
    }}
    
    .distribution-head {{
      display: flex;
      justify-content: space-between;
      font-size: 0.85rem;
      font-weight: 700;
      margin-bottom: 4px;
      color: var(--ink);
    }}
    
    .distribution-track {{
      height: 8px;
      background: rgba(20, 32, 51, 0.06);
      border-radius: 4px;
      overflow: hidden;
    }}
    
    .distribution-fill {{
      height: 100%;
      background: var(--accent);
      border-radius: 4px;
    }}
    
    .source-summary {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    
    .source-highlight {{
      font-size: 0.9rem;
      line-height: 1.6;
      color: var(--muted);
    }}
    
    .source-highlight strong {{
      display: block;
      font-size: 1.1rem;
      color: var(--support);
      font-weight: 800;
    }}
    
    .source-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
    }}
    
    .source-table th, .source-table td {{
      padding: 8px;
      text-align: left;
      border-bottom: 1px solid var(--line);
    }}
    
    .source-table th {{
      color: var(--muted);
      font-weight: 700;
      font-size: 0.75rem;
      text-transform: uppercase;
    }}
    
    .source-filter-button {{
      background: none;
      border: none;
      padding: 0;
      color: var(--ink);
      cursor: pointer;
      font-weight: 700;
      text-align: left;
    }}
    
    .source-filter-button:hover {{
      color: var(--accent);
      text-decoration: underline;
    }}
    
    /* News Feed Layout */
    .grid {{
      display: flex;
      flex-direction: column;
      gap: 28px;
    }}
    
    /* Clean Classic News Card */
    .news-card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 20px;
      padding: 32px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(8px);
    }}
    
    .news-card:hover {{
      border-color: rgba(20, 32, 51, 0.2);
    }}
    
    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }}
    
    .card-index {{
      font-size: 0.85rem;
      font-weight: 800;
      color: var(--support);
      background: rgba(15, 118, 110, 0.08);
      padding: 4px 12px;
      border-radius: 8px;
    }}
    
    .card-top-right {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    
    .source-host {{
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--muted);
    }}
    
    .theme-badge {{
      display: inline-block;
      font-size: 0.78rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--support);
      background: rgba(15, 118, 110, 0.06);
      padding: 4px 10px;
      border-radius: 8px;
      margin-bottom: 16px;
      border: 1px solid rgba(15, 118, 110, 0.12);
    }}
    
    .card-body {{
      color: var(--ink);
      font-size: 1.05rem;
      line-height: 1.7;
      margin-bottom: 20px;
      font-weight: 500;
    }}
    
    .card-expandable {{
      display: none;
      flex-direction: column;
      gap: 24px;
      border-top: 1px solid var(--line);
      padding-top: 24px;
      margin-top: 20px;
    }}
    
    .news-card[data-expanded="true"] .card-expandable {{
      display: flex;
    }}
    
    .insight-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }}
    
    .insight-panel {{
      background: rgba(20, 32, 51, 0.02);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 20px;
    }}
    
    .panel-title {{
      font-size: 0.78rem;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--muted);
      margin: 0 0 12px;
      letter-spacing: 0.06em;
    }}
    
    .insight-tags {{
      margin: 0;
      padding: 0;
      list-style: none;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    
    .insight-tags li {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 0.85rem;
      color: var(--ink);
      font-weight: 600;
    }}
    
    .infographic {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    
    .score-chip {{
      font-size: 0.9rem;
      font-weight: 800;
      color: var(--accent);
      margin-bottom: 4px;
    }}
    
    .metric {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    
    .metric-head {{
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--ink);
    }}
    
    .metric-track {{
      height: 6px;
      background: rgba(20, 32, 51, 0.08);
      border-radius: 3px;
      overflow: hidden;
    }}
    
    .metric-fill {{
      height: 100%;
      background: var(--support);
      border-radius: 3px;
    }}
    
    .summary-list {{
      margin: 0;
      padding-left: 20px;
      color: var(--muted);
      font-size: 0.95rem;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    
    .detail-sections {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }}
    
    .detail-card {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 16px;
    }}
    
    .detail-title {{
      font-size: 0.78rem;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--muted);
      margin: 0 0 8px;
    }}
    
    .detail-copy {{
      font-size: 0.85rem;
      line-height: 1.5;
      margin: 0;
      color: var(--muted);
    }}
    
    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--line);
      padding-top: 20px;
      margin-top: 20px;
    }}
    
    .card-actions {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    
    .source-link {{
      color: var(--accent);
      font-weight: 800;
      text-decoration: none;
      font-size: 0.9rem;
    }}
    
    .source-link:hover {{
      text-decoration: underline;
    }}
    
    .meta-note {{
      font-size: 0.85rem;
      color: var(--muted);
    }}
    
    @media (max-width: 1024px) {{
      .content-layout {{
        grid-template-columns: 1fr;
      }}
      .dashboard-highlights {{
        grid-template-columns: 1fr;
      }}
    }}
    
    @media (max-width: 720px) {{
      .shell {{
        width: min(100% - 24px, 1120px);
        margin-top: 20px;
      }}
      .hero, .news-card {{
        padding: 24px;
        border-radius: 20px;
      }}
      .hero-layout,
      .dashboard-overview,
      .executive-summary,
      .detail-sections,
      .insight-grid {{
        grid-template-columns: 1fr;
      }}
      .commandbar-main,
      .commandbar-actions {{
        flex-direction: column;
        align-items: stretch;
      }}
      .filters-sidebar {{
        position: static;
        max-height: none;
      }}
      .filters-scroll {{
        max-height: none;
      }}
      .card-footer {{
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
      }}
      .toolbar-query-shell {{
        flex-direction: column;
        align-items: stretch;
      }}
      .toolbar-select,
      .button,
      .secondary-button {{
        width: 100%;
      }}
    }}
  </style>
</head>
<body>
  <main class="shell layout-shell">
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
    <section class="content-layout">
      {filters_html}
      <div class="content-stack">
        <section class="portal-commandbar">
          <section class="toolbar">
            <div class="commandbar-main">
              <div id="toolbar-query" class="toolbar-query-shell">
                <span class="toolbar-caption">Komut Arama</span>
                <input id="news-search" class="search-input" type="search" placeholder="Haber metni, kurum, kaynak veya tema ile ara" oninput="filterCards()">
              </div>
              <select id="sort-order" class="toolbar-select" onchange="sortCards()">
                <option value="importance-desc">Oneme Gore</option>
                <option value="relevance">Varsayilan Sira</option>
                <option value="organization-asc">Kuruma Gore</option>
                <option value="theme-asc">Temaya Gore</option>
                <option value="document-asc">Dokumana Gore</option>
              </select>
            </div>
            <div class="commandbar-actions">
              <div id="facet-summary" class="facet-summary">Hazir gorunum: tum akis aktif.</div>
              <div id="results-count" class="chip">{news_count_label}</div>
              <button class="button" type="button" onclick="window.print()">Yazdir veya PDF Al</button>
            </div>
          </section>
        </section>
        <div id="active-filter-chips" class="active-filter-chips" hidden></div>
        {dashboard_html}
        <section class="grid">
          {cards}
        </section>
      </div>
    </section>
  </main>
  <script>
    function applyFilters() {{
      const query = document.getElementById("news-search").value.toLowerCase().trim();
      const organization = document.getElementById("institution-filter").value.toLowerCase().trim();
      const theme = document.getElementById("theme-filter").value.toLowerCase().trim();
      const documentName = document.getElementById("document-filter").value.toLowerCase().trim();
      const source = document.getElementById("source-filter").value.toLowerCase().trim();
      const keyword = document.getElementById("keyword-filter").value.toLowerCase().trim();
      
      const regionField = document.getElementById("region-filter");
      const categoryField = document.getElementById("category-filter");
      const region = regionField ? regionField.value.toLowerCase().trim() : "";
      const category = categoryField ? categoryField.value.toLowerCase().trim() : "";
      
      const cards = Array.from(document.querySelectorAll(".news-card"));
      let visibleCount = 0;

      for (const card of cards) {{
        const haystack = (card.dataset.search || "").toLowerCase();
        const cardOrganization = (card.dataset.organization || "").toLowerCase();
        const cardTheme = (card.dataset.theme || "").toLowerCase();
        const cardDocument = (card.dataset.document || "").toLowerCase();
        const cardSource = (card.dataset.source || "").toLowerCase();
        const keywordHaystack = (card.dataset.keywords || "").toLowerCase();
        const cardRegion = (card.dataset.region || "").toLowerCase();
        const cardCategory = (card.dataset.category || "").toLowerCase();

        const matchesSearch = query === "" || haystack.includes(query);
        const matchesOrganization = organization === "" || cardOrganization === organization;
        const matchesTheme = theme === "" || cardTheme === theme;
        const matchesDocument = documentName === "" || cardDocument === documentName;
        const matchesSource = source === "" || cardSource === source;
        const matchesKeyword = keyword === "" || keywordHaystack.includes(keyword) || haystack.includes(keyword);
        const matchesRegion = region === "" || cardRegion === region;
        const matchesCategory = category === "" || cardCategory === category;

        const visible = matchesSearch && matchesOrganization && matchesTheme && matchesDocument && matchesSource && matchesKeyword && matchesRegion && matchesCategory;
        card.hidden = !visible;
        if (visible) {{
          visibleCount += 1;
        }}
      }}

      document.getElementById("results-count").textContent = "Gosterilen " + visibleCount + " / {len(newsletter.items)} haber";
      syncActiveFilterChips();
      syncFacetState();
      updateFacetSummary(visibleCount);
      syncTOCVisibility();
    }}

    function filterCards() {{
      applyFilters();
    }}

    function sortCards() {{
      const grid = document.querySelector(".grid");
      const cards = Array.from(grid.querySelectorAll(".news-card"));
      const order = document.getElementById("sort-order").value;

      cards.sort((left, right) => {{
        if (order === "importance-desc") {{
          return Number(right.dataset.importance || 0) - Number(left.dataset.importance || 0);
        }}
        if (order === "organization-asc") {{
          return (left.dataset.organization || "").localeCompare(right.dataset.organization || "", "tr");
        }}
        if (order === "theme-asc") {{
          return (left.dataset.theme || "").localeCompare(right.dataset.theme || "", "tr");
        }}
        if (order === "document-asc") {{
          return (left.dataset.documentLabel || "").localeCompare(right.dataset.documentLabel || "", "tr");
        }}
        return Number(left.dataset.index || 0) - Number(right.dataset.index || 0);
      }});

      for (const card of cards) {{
        grid.appendChild(card);
      }}

      applyFilters();
    }}

    function toggleFacetOption(id, value) {{
      const field = document.getElementById(id);
      if (!field) {{
        return;
      }}
      field.value = field.value === value ? "" : value;
      applyFilters();
    }}

    function syncFacetState() {{
      const options = Array.from(document.querySelectorAll(".facet-option"));
      options.forEach((option) => {{
        const field = document.getElementById(option.dataset.facetKey);
        const active = field && field.value === option.dataset.facetValue;
        option.dataset.active = active ? "true" : "false";
      }});

      const activeView = document.body.dataset.activeView || "";
      const viewButtons = Array.from(document.querySelectorAll(".saved-view-button"));
      viewButtons.forEach((button) => {{
        button.dataset.active = button.dataset.view === activeView ? "true" : "false";
      }});
    }}

    function updateFacetSummary(visibleCount) {{
      const ids = ["region-filter", "category-filter", "institution-filter", "theme-filter", "document-filter", "source-filter", "keyword-filter"];
      const active = ids
        .map((id) => document.getElementById(id))
        .filter((field) => field && (field.value || "").trim() !== "");
      const summary = document.getElementById("facet-summary");
      const labels = active.map((field) => field.dataset.label || field.id);
      let text = visibleCount + " haber gorunuyor";
      if (labels.length) {{
        text += " • aktif kirilim: " + labels.join(", ");
      }} else {{
        text += " • tum akisa bakiyorsunuz";
      }}
      summary.textContent = text + ".";
    }}

    function applyPresetView(viewName) {{
      document.body.dataset.activeView = viewName;
      const presets = {{
        operations: {{ sort: "importance-desc", category: "Askeri", theme: "", region: "" }},
        market: {{ sort: "importance-desc", category: "Ekonomik", theme: "", region: "Asya" }},
        platforms: {{ sort: "importance-desc", category: "Teknolojik", theme: "Kurumsal Donusum", region: "ABD" }},
      }};
      const preset = presets[viewName];
      if (!preset) {{
        return;
      }}
      document.getElementById("region-filter").value = preset.region;
      document.getElementById("category-filter").value = preset.category;
      document.getElementById("theme-filter").value = preset.theme;
      document.getElementById("institution-filter").value = "";
      document.getElementById("document-filter").value = "";
      document.getElementById("source-filter").value = "";
      document.getElementById("keyword-filter").value = "";
      document.getElementById("sort-order").value = preset.sort;
      sortCards();
    }}

    function syncActiveFilterChips() {{
      const chipHost = document.getElementById("active-filter-chips");
      const definitions = [
        ["Arama", "news-search"],
        ["Kurum", "institution-filter"],
        ["Tema", "theme-filter"],
        ["Dokuman", "document-filter"],
        ["Kaynak", "source-filter"],
        ["Kelime", "keyword-filter"],
        ["Bolge", "region-filter"],
        ["Kategori", "category-filter"]
      ];
      const chips = [];

      for (const [label, id] of definitions) {{
        const field = document.getElementById(id);
        if (!field) continue;
        const value = (field.value || "").trim();
        if (!value) {{
          continue;
        }}
        chips.push('<span class="active-chip">' + label + ': ' + value + ' <button type="button" onclick="clearFilter(\\'' + id + '\\')">Temizle</button></span>');
      }}

      chipHost.innerHTML = chips.join("");
      chipHost.hidden = chips.length === 0;
    }}

    function syncTOCVisibility() {{
      const cards = Array.from(document.querySelectorAll(".news-card"));
      const visibleIndices = new Set(
        cards.filter(c => !c.hidden).map(c => Number(c.dataset.index) + 1)
      );
      
      const tocItems = Array.from(document.querySelectorAll(".toc-item"));
      tocItems.forEach(item => {{
        const idx = Number(item.dataset.tocIndex);
        if (visibleIndices.has(idx)) {{
          item.style.display = "";
        }} else {{
          item.style.display = "none";
        }}
      }});
      
      const tocGroups = Array.from(document.querySelectorAll(".toc-region-group"));
      tocGroups.forEach(group => {{
        const groupItems = Array.from(group.querySelectorAll(".toc-item"));
        const hasVisible = groupItems.some(item => item.style.display !== "none");
        group.style.display = hasVisible ? "" : "none";
      }});
    }}

    function clearFilter(id) {{
      const field = document.getElementById(id);
      if (field) {{
        field.value = "";
      }}
      if (id === "sort-order") {{
        sortCards();
        return;
      }}
      applyFilters();
    }}

    function setFilterValue(id, value) {{
      const field = document.getElementById(id);
      if (field) {{
        field.value = value;
      }}
      applyFilters();
    }}

    function toggleCardExpansion(cardId) {{
      const card = document.getElementById(cardId);
      const nextState = card.dataset.expanded !== "true";
      card.dataset.expanded = nextState ? "true" : "false";
      const toggle = card.querySelector("[data-expand-toggle]");
      if (toggle) {{
        toggle.textContent = nextState ? "Detayi Daralt" : "Detayi Genislet";
      }}
    }}

    function toggleDashboardSection(sectionKey) {{
      const panel = document.querySelector('[data-collapsible="' + sectionKey + '"]');
      const button = document.querySelector('[data-section-toggle="' + sectionKey + '"]');
      if (!panel || !button) {{
        return;
      }}
      const hidden = !panel.hasAttribute("hidden");
      if (hidden) {{
        panel.setAttribute("hidden", "");
      }} else {{
        panel.removeAttribute("hidden");
      }}
      button.textContent = hidden ? "Genislet" : "Daralt";
      button.setAttribute("aria-expanded", hidden ? "false" : "true");
    }}

    function resetFilters() {{
      document.body.dataset.activeView = "";
      document.getElementById("news-search").value = "";
      document.getElementById("institution-filter").value = "";
      document.getElementById("theme-filter").value = "";
      document.getElementById("document-filter").value = "";
      document.getElementById("source-filter").value = "";
      document.getElementById("keyword-filter").value = "";
      
      const regionField = document.getElementById("region-filter");
      const catField = document.getElementById("category-filter");
      if (regionField) regionField.value = "";
      if (catField) catField.value = "";
      
      document.getElementById("sort-order").value = "importance-desc";
      sortCards();
      applyFilters();
    }}

    sortCards();
  </script>
</body>
</html>
"""


def _render_card(index: int, newsletter: EnrichedNewsletter) -> str:
    item = newsletter.items[index]
    safe_body = escape(item.body)
    safe_url = escape(item.source_url, quote=True)
    host_label = _source_host_label(item.source_url)
    keywords = ", ".join(item.tags)
    search_text = escape(
        " ".join(
            [
                item.body,
                item.headline,
                host_label,
                item.organization_name,
                item.source_document,
                item.theme_name,
                keywords,
                " ".join(item.summary_points),
                item.region,
                item.category,
            ]
        ),
        quote=True,
    )
    safe_host = escape(host_label)
    safe_theme = escape(item.theme_name)
    safe_organization = escape(item.organization_name, quote=True)
    safe_keywords = escape(keywords, quote=True)
    tags_html = "".join(f"<li>{escape(tag)}</li>" for tag in item.tags)
    summary_html = "".join(f"<li>{escape(point)}</li>" for point in item.summary_points)
    detail_sections_html = "".join(
        f'''<article class="detail-card"><h3 class="detail-title">{escape(section.title)}</h3><p class="detail-copy">{escape(section.body)}</p></article>'''
        for section in item.detail_sections
    )
    metrics_html = "".join(_render_metric(metric) for metric in item.infographic_metrics)
    source_document = escape(item.source_document.replace("-", " ").replace("_", " ").title())
    source_document_attr = escape(item.source_document, quote=True)
    safe_theme_attr = escape(item.theme_name, quote=True)
    
    region = escape(item.region)
    category = escape(item.category)

    return f"""<article id="news-{index + 1}" class="news-card" data-search="{search_text}" data-organization="{safe_organization}" data-theme="{safe_theme_attr}" data-document="{source_document_attr}" data-document-label="{source_document}" data-source="{safe_host}" data-keywords="{safe_keywords}" data-importance="{item.importance_score}" data-index="{index}" data-expanded="false" data-region="{region}" data-category="{category}">
  <div class="card-top">
    <div class="card-index">{index + 1:02d}</div>
    <div class="card-top-right">
      <div class="source-host">{safe_host}</div>
      <button class="secondary-button" type="button" data-expand-toggle onclick="toggleCardExpansion('news-{index + 1}')">Detayi Genislet</button>
    </div>
  </div>
  <div class="theme-badge">{safe_theme}</div>
  <div class="card-body">{safe_body}</div>
  <div class="card-expandable">
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
  <section class="insight-panel">
    <p class="panel-title">Habere Iliskin Kisa Degerlendirme</p>
    <div class="detail-sections">{detail_sections_html}</div>
  </section>
  </div>
  <footer class="card-footer">
    <div class="card-actions">
      <a class="source-link" href="{safe_url}" target="_blank" rel="noopener noreferrer">Kaynağı Aç</a>
      <button class="secondary-button" type="button" onclick="setFilterValue('institution-filter', '{escape(item.organization_name, quote=True)}')">Kurumu Filtrele</button>
    </div>
    <span class="meta-note">Kurum: {item.organization_name} | Bölge: {region} | Kategori: {category} | Dokuman: {source_document}</span>
  </footer>
</article>"""


def _render_filters(newsletter: EnrichedNewsletter) -> str:
    organizations = sorted({item.organization_name for item in newsletter.items})
    themes = sorted({item.theme_name for item in newsletter.items})
    documents = sorted({item.source_document for item in newsletter.items})
    sources = sorted({_source_host_label(item.source_url) for item in newsletter.items})
    regions = _ordered_labels(Counter(item.region for item in newsletter.items))
    categories = _ordered_labels(Counter(item.category for item in newsletter.items))
    
    organization_counts = Counter(item.organization_name for item in newsletter.items)
    theme_counts = Counter(item.theme_name for item in newsletter.items)
    document_counts = Counter(item.source_document for item in newsletter.items)
    source_counts = Counter(_source_host_label(item.source_url) for item in newsletter.items)
    tag_counts = Counter(tag for item in newsletter.items for tag in item.tags)
    pills_html = "".join(
        f'<button class="facet-option" type="button" data-facet-key="keyword-filter" data-facet-value="{escape(tag, quote=True)}" onclick="toggleFacetOption(\'keyword-filter\', \'{escape(tag, quote=True)}\')">{escape(tag)} ({count})</button>'
        for tag, _count in tag_counts.most_common(8)
        for count in [tag_counts[tag]]
    )
    stats_html = f"""<div class="filter-stats">
      <div class="filter-stat"><strong>{len(organizations)}</strong><span>Kurum</span></div>
      <div class="filter-stat"><strong>{len(themes)}</strong><span>Tema</span></div>
      <div class="filter-stat"><strong>{len(documents)}</strong><span>Dokuman</span></div>
      <div class="filter-stat"><strong>{len(newsletter.items)}</strong><span>Toplam Haber</span></div>
    </div>"""

    saved_views_html = """
    <div class="saved-view-list">
      <button class="saved-view-button" type="button" data-view="operations" onclick="applyPresetView('operations')">Operasyon</button>
      <button class="saved-view-button" type="button" data-view="market" onclick="applyPresetView('market')">Pazar ve Ekonomi</button>
      <button class="saved-view-button" type="button" data-view="platforms" onclick="applyPresetView('platforms')">Platformlar</button>
    </div>
    """

    return f"""<aside class="dashboard-card filters-sidebar">
  <div class="portal-rail">
  <div class="filters-scroll">
  <div>
    <p class="portal-kicker">Portal Rail</p>
    <h2 class="dashboard-title">Gelismis Filtreler</h2>
    <div class="filter-help">Facet tabanli kirilimlar ile haber akisina kurum, cografya, kategori ve kaynak duzeyinde hizli girin.</div>
  </div>
  <div class="facet-section">
    <span class="filters-label">Kaydedilmis Gorunumler</span>
    {saved_views_html}
  </div>
  {stats_html}
  {_render_facet_section("Coğrafya", "region-filter", regions, Counter(item.region for item in newsletter.items))}
  {_render_facet_section("Tür (Kategori)", "category-filter", categories, Counter(item.category for item in newsletter.items))}
  {_render_facet_section("Kurum", "institution-filter", organizations, organization_counts)}
  {_render_facet_section("Tema", "theme-filter", themes, theme_counts)}
  {_render_facet_section("Dokuman", "document-filter", documents, document_counts, formatter=_document_label)}
  {_render_facet_section("Kaynak Alan Adi", "source-filter", sources, source_counts)}
  <div class="facet-section">
    <span class="filters-label">Hizli Etiketler</span>
    <div class="facet-options">{pills_html}</div>
  </div>
  <div class="filter-state-controls">
    <input id="region-filter" data-label="Bolge" value="">
    <input id="category-filter" data-label="Kategori" value="">
    <input id="institution-filter" data-label="Kurum" value="">
    <input id="theme-filter" data-label="Tema" value="">
    <input id="document-filter" data-label="Dokuman" value="">
    <input id="source-filter" data-label="Kaynak" value="">
    <input id="keyword-filter" data-label="Kelime" value="">
  </div>
  <div class="filters-actions">
    <button class="secondary-button" type="button" style="width: 100%;" onclick="resetFilters()">Filtreleri Temizle</button>
  </div>
  </div>
  </div>
</aside>"""


def _document_label(document_name: str) -> str:
    return document_name.replace("-", " ").replace("_", " ").title()


def _ordered_labels(counter: Counter[str]) -> list[str]:
    preferred_order = ["Türkiye", "Asya", "Avrupa", "ABD", "Küresel", "Siyasi", "Ekonomik", "Askeri", "Teknolojik", "Genel"]
    labels = list(counter.keys())
    rank = {label: index for index, label in enumerate(preferred_order)}
    return sorted(labels, key=lambda label: (rank.get(label, len(preferred_order)), label))


def _render_facet_section(
    title: str,
    field_id: str,
    values: list[str],
    counts: Counter[str],
    *,
    formatter=None,
) -> str:
    option_html = "".join(
        f'<button class="facet-option" type="button" data-facet-key="{field_id}" data-facet-value="{escape(value, quote=True)}" onclick="toggleFacetOption(\'{field_id}\', \'{escape(value, quote=True)}\')">{escape((formatter(value) if formatter else value))} ({counts[value]})</button>'
        for value in values
    )
    return f"""<div class="facet-section">
  <span class="filters-label">{escape(title)}</span>
  <div class="facet-options">{option_html}</div>
</div>"""


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


def _render_toc_grouped(items: list[EnrichedNewsItem]) -> str:
    region_counts = Counter(item.region for item in items)
    regions = _ordered_labels(region_counts)
    grouped = {r: [] for r in regions}
    for idx, item in enumerate(items, start=1):
        r = item.region if item.region in grouped else "Küresel"
        if r not in grouped:
            grouped[r] = []
        grouped[r].append((idx, item))
        
    html = []
    for r in regions:
        region_items = grouped[r]
        if not region_items:
            continue
        html.append(f'<div class="toc-region-group">')
        html.append(f'<div class="toc-region-title">{escape(r)}</div>')
        html.append('<div class="toc-region-items">')
        for idx, item in region_items:
            html.append(f"""
            <a class="toc-item" href="#news-{idx}" data-toc-index="{idx}">
                <div class="toc-item-headline">Haber {idx:02d} / {escape(item.headline)}</div>
                <div class="toc-item-meta">
                    <span class="toc-org">{escape(item.organization_name)}</span>
                    <span class="toc-cat">{escape(item.category)}</span>
                </div>
            </a>
            """)
        html.append('</div>')
        html.append('</div>')
    return "\n".join(html)


def _render_dashboard(newsletter: EnrichedNewsletter) -> str:
    toc_html = _render_toc_grouped(newsletter.items)
    avg_importance = round(sum(item.importance_score for item in newsletter.items) / max(len(newsletter.items), 1))
    theme_counts = Counter(item.theme_name for item in newsletter.items)
    source_counts = Counter(_source_host_label(item.source_url) for item in newsletter.items)
    total_items = max(len(newsletter.items), 1)

    theme_distribution = "".join(
        _render_distribution_row(theme, count, total_items) for theme, count in theme_counts.most_common()
    )
    source_rows = "".join(
        f"""<tr>
          <td><button class="source-filter-button" type="button" data-source-filter="{escape(host, quote=True)}" onclick="setFilterValue('source-filter', '{escape(host, quote=True)}')">{escape(host)}</button></td>
          <td>{count}</td>
          <td>%{round(count / total_items * 100)}</td>
        </tr>"""
        for host, count in source_counts.most_common()
    )

    top_tag_count = len({tag for item in newsletter.items for tag in item.tags})
    avg_metrics = [metric.value for item in newsletter.items for metric in item.infographic_metrics]
    heat_index = round(sum(avg_metrics) / max(len(avg_metrics), 1))
    dominant_theme, dominant_theme_count = theme_counts.most_common(1)[0]
    top_source, top_source_count = source_counts.most_common(1)[0]
    organizations = sorted({item.organization_name for item in newsletter.items})
    executive_points = [
        f"Toplam {len(newsletter.items)} haber, {len(organizations)} farklı kurum ve {len(theme_counts)} tema altında toplandı.",
        f"Baskın tema {dominant_theme}; toplam havuz içindeki payı {domin_theme_pct(dominant_theme_count, total_items)} seviyesinde.",
        f"Kaynak akışında {top_source} baskın; izleme yoğunluğu bu alanda toplanmış durumda.",
    ]
    executive_copy = (
        f"Bu hafta öne çıkan gelişmeler ağırlıklı olarak {escape(dominant_theme.lower())} ekseninde toplandı. "
        f"Okuma havuzu {escape(', '.join(organizations))} kurumları üzerinde yoğunlaşırken, yönetici takibi için tema dağılımı ve kaynak akışı birlikte izlenmeli."
    )

    return f"""<section class="dashboard">
  <section class="dashboard-overview">
    <article class="overview-stat">
      <p class="overview-label">Toplam Haber</p>
      <div class="overview-value">{len(newsletter.items)}</div>
      <div class="overview-note">Tek sayfada toplanan toplam kayit.</div>
    </article>
    <article class="overview-stat">
      <p class="overview-label">Ortalama Onem</p>
      <div class="overview-value">{avg_importance}</div>
      <div class="overview-note">Genel kurumsal etki seviyesi.</div>
    </article>
    <article class="overview-stat">
      <p class="overview-label">Baskin Tema</p>
      <div class="overview-value">{escape(dominant_theme)}</div>
      <div class="overview-note">{dominant_theme_count} haber ile en yogun konu.</div>
    </article>
    <article class="overview-stat">
      <p class="overview-label">Baskin Kaynak</p>
      <div class="overview-value">{escape(top_source)}</div>
      <div class="overview-note">%{round(top_source_count / total_items * 100)} pay ile en cok gecen alan adi.</div>
    </article>
  </section>
  <section class="dashboard-card executive-summary">
    <div>
      <h2 class="dashboard-title">Yonetici Ozeti</h2>
      <p class="executive-copy">{executive_copy}</p>
    </div>
    <div>
      <h2 class="dashboard-title">Bu hafta one cikan gelismeler</h2>
      <ul class="executive-list">{''.join(f'<li>{escape(point)}</li>' for point in executive_points)}</ul>
    </div>
  </section>
  <section class="dashboard-highlights">
    <section class="dashboard-primary">
      <div class="dashboard-card compact">
        <div class="dashboard-card-head">
          <h2 class="dashboard-title">Icerik Indeksi</h2>
          <button class="dashboard-toggle" type="button" data-section-toggle="toc" aria-expanded="false" onclick="toggleDashboardSection('toc')">Genislet</button>
        </div>
        <div class="collapsible-panel" data-collapsible="toc" hidden>
          <div class="toc-list">{toc_html}</div>
        </div>
      </div>
      <div class="dashboard-metrics">
        <section class="dashboard-card compact">
          <div class="radar-card">
            <h2 class="dashboard-title">Gundem Nabzi</h2>
            <div class="radial-stat">
              <div class="radial-ring" style="--value: {avg_importance}">
                <span>{avg_importance}</span>
              </div>
              <div class="radial-copy">Onem skoru, etiket yogunlugu ve operasyon baglamini tek bakista ozetler.</div>
            </div>
            <div class="stat-strip">
              <div class="mini-stat"><strong>{top_tag_count}</strong><span>Aktif Etiket</span></div>
              <div class="mini-stat"><strong>{heat_index}</strong><span>Gundem Indeksi</span></div>
              <div class="mini-stat"><strong>{len(theme_counts)}</strong><span>Tema Sayisi</span></div>
            </div>
          </div>
        </section>
      </div>
    </section>
    <section class="dashboard-secondary">
      <section class="dashboard-card compact">
        <h2 class="dashboard-title">Tema Dagilimi</h2>
        <div class="distribution-list">{theme_distribution}</div>
      </section>
      <section class="dashboard-card compact">
        <h2 class="dashboard-title">Kaynak Yogunlugu</h2>
        <div class="source-summary">
          <div class="source-highlight">
            <strong>{escape(top_source)}</strong>
            <span>En baskin alan adi. Toplam {top_source_count} haber ve %{round(top_source_count / total_items * 100)} pay.</span>
          </div>
          <table class="source-table">
            <thead><tr><th>Kaynak</th><th>Adet</th><th>Pay</th></tr></thead>
            <tbody>{source_rows}</tbody>
          </table>
        </div>
      </section>
    </section>
  </section>
</section>"""


def domin_theme_pct(count: int, total_items: int) -> str:
    return f"%{round(count / total_items * 100)}"


def _render_distribution_row(label: str, count: int, total_items: int) -> str:
    percentage = round(count / total_items * 100)
    return f"""<div class="distribution-row">
  <button class="distribution-button" type="button" data-theme-filter="{escape(label, quote=True)}" onclick="setFilterValue('theme-filter', '{escape(label, quote=True)}')">
    <div class="distribution-head">
      <span>{escape(label)}</span>
      <span>%{percentage}</span>
    </div>
    <div class="distribution-track">
      <div class="distribution-fill" style="width: {percentage}%"></div>
    </div>
  </button>
</div>"""
