from typing import List
from scraper.sources.base import BaseSource
from scraper.parsers.listing_parser import ListingParser


class MudahSource(BaseSource):
    name = "mudah"

    SEARCHES = [
        "apartment for sale",
        "2 story house",
        "1 story house",
        "bungalow house",
        "property for sale"
    ]

    async def fetch_listings(self, state: str) -> List[str]:

        all_urls = []

        for query in self.SEARCHES:

            url = f"https://www.mudah.my/malaysia/properties-for-sale?q={state}+{query}"

            html = await self.client.get_html(url)

            if not html or len(html) < 1000:
                continue

            # IMPORTANT: wait for JS render (FIX #1)

            urls = ListingParser.extract_urls(html, self.name)

            all_urls.extend(urls)

        # dedupe
        return list(dict.fromkeys(all_urls))