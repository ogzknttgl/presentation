# 2026-06-20 Interactive Dashboard Pass

## Issue 1: Active filter state is invisible
- Users can set multiple filters but cannot see the current state compactly.
- Add active filter chips with one-click removal.

## Issue 2: Cards are always fully expanded
- Long reports become visually heavy.
- Add expand/collapse behavior per card so scanning is easier.

## Issue 3: No sorting controls
- Users cannot reprioritize the reading order by importance, institution, theme, or source document.
- Add a sorting dropdown that works fully offline.

## Issue 4: Dashboard panels are read-only
- Theme distribution and source density should directly drive the filtered result set.
- Make those dashboard surfaces clickable and connected to filters.

## Issue 5: No executive quick-read mode
- Managers need a short, high-signal pass without reading all cards.
- Add a `Yöneticinin 5 dakikalık görünümü` toggle that narrows to the most important items.

## Implementation Status
- Added visible active filter chips with one-click clearing for search, institution, theme, document, source, and keyword state.
- Added per-card `Detayi Genislet` and `Detayi Daralt` behavior with collapsed default state to reduce visual density.
- Added offline sorting controls for importance, institution, theme, document, and default order.
- Converted theme distribution and source density surfaces into clickable filters wired to the sidebar state.
- Added `Yonetici 5 Dakika` mode to compress the page into a faster scan path focused on the top visible items.
