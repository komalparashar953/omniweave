from app.scraper.static import scrape_static
from app.scraper.dynamic import scrape_dynamic
from app.models import ScrapeResult

async def scrape_url(url: str) -> ScrapeResult:
    # 1. Try Scrape Static
    try:
        print(f"Attempting static scrape for {url}")
        result = await scrape_static(url)
        print("Static scrape successful")
        return result
    except Exception as e:
        print(f"Static scrape failed or insufficient: {e}")
    
    # 2. Fallback to Dynamic
    print(f"Attempting dynamic scrape for {url}")
    result = await scrape_dynamic(url)
    return result
