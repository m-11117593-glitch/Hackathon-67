import asyncio
import logging

from scraper.browser.playwright_client import PlaywrightClient
from scraper.parsers.listing_parser import ListingParser
from scraper.parsers.detail_parser import DetailParser

from scraper.utils.query_builder import build_search_url
from scraper.live.search_fallback import generate_query_variants
from scraper.utils.temp_cache import save_temp_results

logger = logging.getLogger(__name__)

MAX_RESULTS = 50


async def scrape_search_page(client, url):

    try:
        html = await client.get_html(url)

        if not html:
            return []

        return ListingParser.extract_urls(html, "live_search")

    except Exception as e:
        logger.warning(f"Search page failed: {e}")
        return []


async def scrape_property_detail(client, url, filters):

    try:
        html = await client.get_html(url)

        if not html:
            return None

        return DetailParser.extract_data(
            html,
            url,
            "live_search",
            filters["location"],
            filters.get("listing_type", "sale")
        )

    except Exception as e:
        logger.warning(f"Detail scrape failed: {e}")
        return None


async def live_property_search(filters: dict):

    logger.info(f"Starting live search: {filters}")

    client = PlaywrightClient()
    await client.start()

    try:

        variants = generate_query_variants(filters)

        all_listing_urls = []

        for i, variant in enumerate(variants):

            base_url = build_search_url(variant)

            variant_urls = []

            for page in range(1, 3):

                if page == 1:
                    page_url = base_url
                else:
                    sep = "&" if "?" in base_url else "?"
                    page_url = f"{base_url}{sep}o={page}"

                urls = await scrape_search_page(client, page_url)
                variant_urls.extend(urls)

            variant_urls = list(dict.fromkeys(variant_urls))

            if len(variant_urls) >= 10:
                all_listing_urls = variant_urls
                break

            all_listing_urls.extend(variant_urls)

        unique_urls = list(dict.fromkeys(all_listing_urls))[:50]

        tasks = [
            scrape_property_detail(client, url, filters)
            for url in unique_urls
        ]

        results = await asyncio.gather(*tasks)
        results = [r for r in results if r]

        payload = {
            "success": True,
            "total_results": len(results),
            "filters_used": filters,
            "results": results
        }

        json_path = save_temp_results(payload)
        payload["json_path"] = json_path

        return payload

    finally:
        await client.stop()