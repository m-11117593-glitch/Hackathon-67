import asyncio
import logging

from scraper.browser.playwright_client import PlaywrightClient
from scraper.parsers.listing_parser import ListingParser
from scraper.parsers.detail_parser import DetailParser

from scraper.utils.query_builder import build_search_url
from scraper.utils.temp_cache import save_temp_results

logger = logging.getLogger(__name__)


MAX_PAGES = 3

MAX_RESULTS = 50


async def scrape_search_page(
    client,
    url
):

    try:

        html = await client.get_html(url)

        if not html:
            return []

        urls = ListingParser.extract_urls(
            html,
            "live_search"
        )

        return urls

    except Exception as e:

        logger.warning(
            f"Search page failed: {e}"
        )
        print("\nGENERATED URL:")
        print(base_url)
        print()
        return []


async def scrape_property_detail(
    client,
    url,
    filters
):

    try:

        html = await client.get_html(url)

        if not html:
            return None

        data = DetailParser.extract_data(
            html=html,
            url=url,
            source="mudah_live",
            state=filters.get("location", "malaysia")
        )

        return data

    except Exception as e:

        logger.warning(
            f"Detail scrape failed: {e}"
        )

        return None


async def live_property_search(filters: dict):

    logger.info(f"Starting live search: {filters}")

    client = PlaywrightClient()
    await client.start()

    try:

        from scraper.utils.query_builder import build_search_url
        from scraper.live.search_fallback import generate_query_variants

        variants = generate_query_variants(filters)

        all_listing_urls = []
        all_results = []

        # =====================================================
        # LOOP THROUGH FALLBACK STRATEGY
        # =====================================================
        for i, variant in enumerate(variants):

            logger.info(f"Search variant {i+1}: {variant}")

            base_url = build_search_url(variant)

            logger.info(f"Generated URL: {base_url}")

            # reset per variant
            variant_urls = []

            # ---------------- PAGINATION ----------------
            for page in range(1, 3):  # keep fast

                if page == 1:
                    page_url = base_url
                else:
                    separator = "&" if "?" in base_url else "?"
                    page_url = f"{base_url}{separator}o={page}"

                urls = await scrape_search_page(client, page_url)

                variant_urls.extend(urls)

            # dedupe variant
            variant_urls = list(dict.fromkeys(variant_urls))

            logger.info(f"Variant {i+1} URLs: {len(variant_urls)}")

            # ---------------- STOP EARLY IF GOOD ENOUGH ----------------
            if len(variant_urls) >= 10:
                all_listing_urls = variant_urls
                logger.info("Good result found, stopping fallback chain")
                break

            # otherwise accumulate
            all_listing_urls.extend(variant_urls)

        # ---------------- FINAL DEDUPE ----------------
        unique_urls = list(dict.fromkeys(all_listing_urls))[:50]

        logger.info(f"Final URLs: {len(unique_urls)}")

        # ---------------- SCRAPE DETAILS ----------------
        tasks = [
            scrape_property_detail(client, url, filters)
            for url in unique_urls
        ]

        results = await asyncio.gather(*tasks)
        results = [r for r in results if r]

        logger.info(f"Final results: {len(results)}")

        # ---------------- SAVE JSON ----------------
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