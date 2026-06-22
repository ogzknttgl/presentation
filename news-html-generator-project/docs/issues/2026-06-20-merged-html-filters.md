# 2026-06-20 Merged HTML and Filters

## Issue 1: Directory input cannot produce a single merged HTML output
- Current behavior writes one HTML per DOCX plus an index page.
- Requested behavior is a single HTML file that reads multiple `.docx` inputs and merges all news cards into one page.
- CLI dispatch currently treats directory input as "site package" mode only.

## Issue 2: Search only checks body text and source host
- Current search uses `data-search` built from `item.body` and URL host only.
- Institution, document source, theme, tags, and summary keywords are excluded from the search index.
- This makes valid user queries appear broken.

## Issue 3: No left-side advanced filtering UI
- The current page has a top toolbar only.
- Requested behavior needs a persistent left menu for advanced filters.
- Filters should support at least institution-based filtering and content keyword filtering.

## Issue 4: Renderer lacks metadata needed for multi-document filtering
- `EnrichedNewsItem` has no document-level source metadata.
- The HTML cannot filter by institution or originating DOCX because those values are not carried into card datasets.

## Issue 5: Documentation describes only per-file and package output modes
- README does not describe merged single-file generation for multiple DOCX inputs.
- Expected CLI behavior and output modes need to be documented after implementation.
