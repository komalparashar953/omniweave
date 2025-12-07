from playwright.async_api import async_playwright, Page
from app.scraper.parser import parse_html, extract_meta
from app.models import ScrapeResult, Interactions, Section, Error
from datetime import datetime
import asyncio
from typing import List

async def scroll_and_wait(page: Page, count: int = 3) -> int:
    scrolls = 0
    for _ in range(count):
        try:
            # Scroll to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            # Wait for network idle or timeout
            await page.wait_for_load_state("networkidle", timeout=3000)
            await asyncio.sleep(1) # Extra stability wait
            scrolls += 1
        except Exception:
            break
    return scrolls

async def click_interactions(page: Page) -> List[str]:
    clicks = []
    # Heuristic selectors for "Load More" or Tabs
    selectors = [
        "button:has-text('Load more')",
        "button:has-text('Show more')",
        "[role='tab']",
        ".load-more",
        "#load-more"
    ]
    
    for selector in selectors:
        try:
            # Check if visible
            if await page.is_visible(selector):
                await page.click(selector, timeout=2000)
                await page.wait_for_load_state("networkidle", timeout=3000)
                clicks.append(selector)
                if len(clicks) >= 3: break # Limit interactions
        except Exception:
            continue
            
    return clicks

async def scrape_dynamic(url: str) -> ScrapeResult:
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="UniversalScraper/1.0")
        page = await context.new_page()
        
        errors = []
        interaction_log = Interactions(clicks=[], scrolls=0, pages=[url])

        try:
            # Navigation
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                await page.wait_for_load_state("networkidle", timeout=5000)
            except Exception as e:
                errors.append(Error(message=str(e), phase="navigation"))

            # Interactions
            try:
                # 1. Clicks
                clicks = await click_interactions(page)
                interaction_log.clicks.extend(clicks)
                
                # 2. Scrolling
                scrolls = await scroll_and_wait(page, count=3)
                interaction_log.scrolls = scrolls
                
                # 3. Pagination (Naive check for next page params or URL changes not easily done without more logic, 
                # so we stick to scroll/click primarily as requested per simplistic infinite scroll/pagination view)
            except Exception as e:
                errors.append(Error(message=str(e), phase="interaction"))

            # Capture Content
            html = await page.content()
            meta = extract_meta(html, url)
            sections = parse_html(html, url)
            
        except Exception as e:
            errors.append(Error(message=f"Critical failure: {str(e)}", phase="run"))
            html = ""
            meta = {}
            sections = []
        finally:
            await browser.close()

        return ScrapeResult(
            url=url,
            scrapedAt=datetime.utcnow(),
            meta=meta,
            sections=sections,
            interactions=interaction_log,
            errors=errors
        )
