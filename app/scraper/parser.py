from bs4 import BeautifulSoup, Tag
from app.models import Section, SectionContent, Link, Image
from typing import List, Optional
import uuid

def derive_label(text: str) -> str:
    """Derive a label from the first few words of the text."""
    words = text.split()[:7]
    return " ".join(words) + ("..." if len(words) >= 7 else "")

def parse_html(html: str, url: str) -> List[Section]:
    soup = BeautifulSoup(html, "html.parser")
    sections = []

    # Strategy 1: Look for semantic tags
    semantic_tags = ["header", "nav", "main", "section", "article", "footer", "aside"]
    elements = soup.find_all(semantic_tags)

    if not elements:
        # Fallback: Body children that are block elements
        elements = [child for child in soup.body.children if isinstance(child, Tag) and child.name in ["div", "div"]]

    for idx, el in enumerate(elements):
        # Extract content
        headings = [h.get_text(strip=True) for h in el.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
        
        # Text extraction (naive)
        text = el.get_text(" ", strip=True)
        
        # Links
        links = []
        for a in el.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/"):
                # Handle relative URLs naively (better to use urljoin in real impl)
                from urllib.parse import urljoin
                href = urljoin(url, href)
            links.append(Link(text=a.get_text(strip=True), href=href))

        # Images
        images = []
        for img in el.find_all("img", src=True):
            src = img["src"]
            if src.startswith("/"):
                from urllib.parse import urljoin
                src = urljoin(url, src)
            images.append(Image(src=src, alt=img.get("alt", "")))

        # Lists
        lists = []
        for ul in el.find_all(["ul", "ol"]):
            items = [li.get_text(strip=True) for li in ul.find_all("li")]
            if items:
                lists.append(items)

        # Tables (basic text extraction)
        tables = []
        for table in el.find_all("table"):
            rows = []
            for tr in table.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                rows.append(cols)
            if rows:
                tables.append(rows)

        # Skip empty sections
        if not text and not images and not links:
            continue

        # Label
        label = "Section"
        if headings:
            label = headings[0]
        elif text:
            label = derive_label(text)
        
        # Type
        section_type = el.name if el.name in semantic_tags else "section"
        if section_type == "header": section_type = "hero" # Approximation

        raw_html = str(el)
        truncated = len(raw_html) > 1000
        if truncated:
            raw_html = raw_html[:1000] + "..."

        section = Section(
            id=f"{section_type}-{idx}-{uuid.uuid4().hex[:6]}",
            type=section_type,
            label=label,
            sourceUrl=url,
            content=SectionContent(
                headings=headings,
                text=text[:5000], # Limit text length
                links=links[:50], # Limit links
                images=images[:20],
                lists=lists,
                tables=tables
            ),
            rawHtml=raw_html,
            truncated=truncated
        )
        sections.append(section)

    return sections

def extract_meta(html: str, url: str):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else ""
    
    description = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        description = meta_desc.get("content", "")
    
    lang = "en"
    if soup.html and soup.html.get("lang"):
        lang = soup.html["lang"]
        
    canonical = None
    link_canon = soup.find("link", rel="canonical")
    if link_canon:
        canonical = link_canon.get("href")

    return {
        "title": title,
        "description": description,
        "language": lang,
        "canonical": canonical
    }
