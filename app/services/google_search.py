import os
from typing import List, Optional
from httpx import AsyncClient
from app.schemas import SearchResult

GOOGLE_API_URL = "https://www.googleapis.com/customsearch/v1"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

async def google_search(client: AsyncClient, q: str, num: int = 10, site: Optional[str] = None) -> List[SearchResult]:
    """
    Perform a Google Custom Search (Programmable Search) query.
    If `site` is provided, the search will be restricted to that site.
    Requires GOOGLE_API_KEY and GOOGLE_CSE_ID env vars to be set.
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        raise RuntimeError("Missing GOOGLE_API_KEY or GOOGLE_CSE_ID environment variables")

    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": q,
        "num": max(1, min(num, 10)),  # Google CSE commonly limited to 10 per request
    }
    if site:
        # Restrict search to a single site
        params["siteSearch"] = site
        params["siteSearchFilter"] = "i"  # include only results from this site

    resp = await client.get(GOOGLE_API_URL, params=params, timeout=15.0)
    resp.raise_for_status()
    data = resp.json()
    raw_items = data.get("items", []) or []

    results: List[SearchResult] = []
    for idx, it in enumerate(raw_items, start=1):
        title = it.get("title", "")
        snippet = it.get("snippet") or it.get("snippetAlt") or None
        link = it.get("link")
        if not link:
            continue
        results.append(
            SearchResult(
                title=title,
                snippet=snippet,
                link=link,
                source=site or "google",
                position=idx,
            )
        )
    return results
