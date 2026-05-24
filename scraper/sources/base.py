from typing import List, Dict, Any
import logging

from scraper.parsers.listing_parser import ListingParser
from scraper.parsers.detail_parser import DetailParser

logger = logging.getLogger(__name__)


class BaseSource:

    name = "base"

    def __init__(self, client):
        self.client = client

    # must be overridden in mudah_config source
    def get_page_url(self, state: str, page: int) -> str:
        raise NotImplementedError

    # -----------------------------
    # FIXED LISTING FETCH
    # -----------------------------
    async def fetch_listings(self, state: str) -> List[str]:

        all_urls = []

        for page in range(1, 6):

            try:
                url = self.get_page_url(state, page)

                html = await self.client.get_html(url)

                if not html:
                    continue

                page_urls = ListingParser.extract_urls(html, self.name)

                logger.info(f"[{self.name}] page {page}: {len(page_urls)} listings")

                # 🔥 FORCE STRING ONLY (CRITICAL FIX)
                for u in page_urls:

                    if isinstance(u, dict):
                        u = u.get("url")

                    if isinstance(u, str) and u.startswith("http"):
                        all_urls.append(u)

            except Exception as e:
                logger.warning(f"[{self.name}] page {page} failed: {e}")

        # -----------------------------
        # DEDUPE FIX (NO DICT SET CRASH)
        # -----------------------------
        seen = set()
        final = []

        for url in all_urls:

            if not isinstance(url, str):
                continue

            if url in seen:
                continue

            seen.add(url)
            final.append(url)

        return final

    # -----------------------------
    # DETAIL SCRAPE
    # -----------------------------
    async def scrape_detail(self, url: str, state: str) -> Dict[str, Any]:

        html = await self.client.get_html(url)

        return DetailParser.extract_data(
            html,
            url,
            self.name,
            state
        )