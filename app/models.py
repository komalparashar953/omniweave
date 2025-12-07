from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, HttpUrl, Field

class ScrapeRequest(BaseModel):
    url: HttpUrl

class Meta(BaseModel):
    title: Optional[str] = ""
    description: Optional[str] = ""
    language: Optional[str] = "en"
    canonical: Optional[str] = None

class Link(BaseModel):
    text: str
    href: str

class Image(BaseModel):
    src: str
    alt: str

class SectionContent(BaseModel):
    headings: List[str] = []
    text: str = ""
    links: List[Link] = []
    images: List[Image] = []
    lists: List[List[str]] = []
    tables: List[List[Any]] = []

class Section(BaseModel):
    id: str
    type: str  # hero | section | nav | footer | list | grid | faq | pricing | unknown
    label: str
    sourceUrl: str
    content: SectionContent
    rawHtml: str
    truncated: bool

class Interactions(BaseModel):
    clicks: List[str] = []
    scrolls: int = 0
    pages: List[str] = []

class Error(BaseModel):
    message: str
    phase: str

class ScrapeResult(BaseModel):
    url: str
    scrapedAt: datetime
    meta: Meta
    sections: List[Section]
    interactions: Interactions
    errors: List[Error] = []

class ScrapeResponse(BaseModel):
    result: ScrapeResult
