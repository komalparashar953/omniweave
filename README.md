# OmniWeave

A universal website scraper with a JSON viewer frontend. **OmniWeave** turns the chaotic web into structured, beautiful JSON.

## Setup and Run

1.  Ensure you have Python 3.10+ installed.
2.  Open a terminal (Git Bash or similar on Windows, or standard terminal on Linux/Mac).
3.  Run the following commands:

```bash
chmod +x run.sh
./run.sh
```

This will:
- Create a virtual environment.
- Install dependencies.
- Install Playwright browsers.
- Start the server at `http://localhost:8000`.

## Testing URLs

1.  **Static**: `https://en.wikipedia.org/wiki/Artificial_intelligence` - Large static content.
2.  **JS/Tabs**: `https://vercel.com/` - React-heavy, uses tabs.
3.  **Pagination/Scroll**: `https://news.ycombinator.com/` - Pagination.

## Known Limitations

-   Depth is strictly limited to prevent long execution times.
-   Very complex SPAs with obscure anti-bot measures might still block the scraper.
