import httpx
from app.scraper.parser import parse_html, extract_meta
from app.models import ScrapeResult, Interactions
from datetime import datetime

async def scrape_static(url: str) -> ScrapeResult:
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        try:
            response = await client.get(url, headers={"User-Agent": "UniversalScraper/1.0"})
            response.raise_for_status()
        except Exception as e:
            # Re-raise or handle gracefully. For now, let's propagate to caller to decide fallback
            raise e

    html = response.text
    meta = extract_meta(html, url)
    sections = parse_html(html, url)

    # Basic check for emptiness to trigger fallback
    if len(html) < 500 or not sections:
        raise ValueError("Insufficient content, trigger fallback")

    return ScrapeResult(
        url=url,
        scrapedAt=datetime.utcnow(),
        meta=meta,
        sections=sections,
        interactions=Interactions(clicks=[], scrolls=0, pages=[url]),
        errors=[]
    )
