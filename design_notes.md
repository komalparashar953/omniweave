# Design Notes

## Static vs JS Fallback
- Strategy: We attempt to scrape the page using `httpx` first. If the returned HTML body is too short (e.g., < 500 characters) or is missing a `<main>` or `<body>` tag with substantial content, we infer that the page is JS-rendered and switch to Playwright.

## Wait Strategy for JS
- [x] Network idle
- [ ] Fixed sleep
- [x] Wait for selectors
- Details: We use `page.goto(url, wait_until="networkidle")` to ensure the initial load is complete. For interactions, we wait for the DOM to settle after clicks or scrolls.

## Click & Scroll Strategy
- Click flows implemented: We look for elements matching typical "Load More", "Show More" text or `[role="tab"]` attributes and attempt to click them.
- Scroll / pagination approach: We scroll to the bottom of the page 3 times, waiting for network idle in between.
- Stop conditions: Max 3 interactions/scrolls or if no new content is detected.

## Section Grouping & Labels
- How you group DOM into sections: We use semantic tags like `<section>`, `<article>`, `<header>`, `<footer>`. If those aren't precise, we fallback to dividing content by `<h1>`-`<h6>` tags.
- How you derive section `type` and `label`: `type` is inferred from the tag name (e.g., `<nav>` -> `nav`, `<footer>` -> `footer`). `label` is taken from the first heading within the section or the first few words of text.

## Noise Filtering & Truncation
- What you filter out: We remove `<script>`, `<style>`, `<noscript>`, and elements with classes/ids indicating cookie banners or ads.
- How you truncate `rawHtml` and set `truncated`: We keep the first 1000 characters of the raw HTML for each section and set `truncated: true` if it exceeds that.
