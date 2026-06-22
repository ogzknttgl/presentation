# Merged HTML Filters Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add support for converting multiple `.docx` files into one offline HTML bulletin with left-side advanced filters and reliable search.

**Architecture:** Keep parsing and enrichment rule-based and offline. Introduce a merged-newsletter aggregation layer that normalizes document-level metadata, then render a unified HTML experience whose search and filters operate on per-card datasets generated from both document and content metadata.

**Tech Stack:** Python, standard library, inline HTML/CSS/JavaScript, `unittest`

---

## Chunk 1: Data and generator changes

### Task 1: Define merged-output behavior in tests

**Files:**
- Modify: `tests/test_generator.py`
- Test: `tests/test_generator.py`

- [ ] **Step 1: Write a failing test for merged directory input**
- [ ] **Step 2: Run the targeted test and confirm the expected failure**
- [ ] **Step 3: Implement the minimal aggregation and generator API**
- [ ] **Step 4: Re-run the targeted test and confirm it passes**

### Task 2: Carry document-level metadata into rendered cards

**Files:**
- Modify: `src/news_html_generator/models.py`
- Modify: `src/news_html_generator/enrichment.py`
- Modify: `tests/test_generator.py`

- [ ] **Step 1: Write a failing test asserting institution/source metadata appears in merged output**
- [ ] **Step 2: Run the targeted test and confirm the expected failure**
- [ ] **Step 3: Add minimal metadata fields needed for rendering/filtering**
- [ ] **Step 4: Re-run the targeted test and confirm it passes**

## Chunk 2: Filter/search rendering

### Task 3: Add failing coverage for advanced filters and improved search

**Files:**
- Modify: `tests/test_generator.py`
- Modify: `src/news_html_generator/renderer.py`

- [ ] **Step 1: Write failing assertions for left filter panel, keyword filter inputs, and broader search dataset**
- [ ] **Step 2: Run the targeted test and confirm the expected failure**
- [ ] **Step 3: Implement minimal renderer and inline-JS changes**
- [ ] **Step 4: Re-run the targeted test and confirm it passes**

## Chunk 3: CLI and docs

### Task 4: Make CLI route directory + `.html` output to merged mode

**Files:**
- Modify: `src/news_html_generator/cli.py`
- Modify: `tests/test_generator.py`

- [ ] **Step 1: Write failing coverage for directory-to-single-html behavior**
- [ ] **Step 2: Run the targeted test and confirm the expected failure**
- [ ] **Step 3: Implement minimal CLI dispatch changes**
- [ ] **Step 4: Re-run the targeted test and confirm it passes**

### Task 5: Update docs after behavior is green

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Document merged HTML mode and package mode separately**
- [ ] **Step 2: Run the full test suite**
- [ ] **Step 3: Confirm output is green and consistent with docs**
