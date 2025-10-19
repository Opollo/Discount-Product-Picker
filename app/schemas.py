from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime, timezone

class SearchResult(BaseModel):
    title: str
    snippet: Optional[str] = None
    link: HttpUrl
    source: str  # e.g. "google", or site like "jumia.com"
    position: Optional[int] = None  # 1-based rank in the single result list
    fetched_at: datetime = datetime.now(timezone.utc)

class AggregatedResult(BaseModel):
    title: str
    link: HttpUrl
    sources: List[str]  # sites where this link appeared
    occurrences: int
    avg_position: float
    snippet: Optional[str] = None
    fetched_at: datetime = datetime.now(timezone.utc)