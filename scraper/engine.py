import asyncio
import logging
import json
import time

from pathlib import Path

from scraper.browser.playwright_client import PlaywrightClient
from scraper.parsers.listing_parser import ListingParser
from scraper.parsers.detail_parser import DetailParser
from scraper.utils.query_builder import build_search_url

logger = logging.getLogger(__name__)

CACHE_DIR = Path("cache")
HISTORY_DIR = CACHE_DIR / "history"

TTL_SECONDS = 60 * 60 * 24 * 3


def ensure_dirs():
    HISTORY_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def save_json(path, data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def cleanup_old_cache():

    now = time.time()

    for file in HISTORY_DIR.glob("*.json"):

        try:

            ts = float(file.stem)

            if now - ts > TTL_SECONDS:

                file.unlink()

                logger.info(
                    f"🧹 Deleted old cache: {file.name}"
                )

        except:
            pass


def deduplicate(listings):

    seen = set()
    clean = []

    for item in listings:

        url = item.get("url")

        if not url:
            continue

        if url in seen:
            continue

        seen.add(url)

        clean.append(item)

    return clean


async def scrape_properties(filters: dict):

    ensure_dirs()

    listing_type = filters.get(
        "listing_type",
        "sale"
    )

    state = filters.get(
        "location",
        "malaysia"
    )

    client = PlaywrightClient()

    await client.start()

    try:

        logger.info(
            f"🚀 Scraping {listing_type}: {state}"
        )

        all_urls = []
        seen = set()

        # ---------------- SEARCH PAGES ----------------
        for page in range(1, 4):

            search_url = build_search_url(
                filters,
                page
            )

            logger.info(
                f"📦 Search Page: {search_url}"
            )

            html = await client.get_html(
                search_url
            )

            if not html:
                continue

            urls = ListingParser.extract_urls(
                html,
                listing_type
            )

            if not urls:
                break

            for u in urls:

                if u not in seen:
                    seen.add(u)
                    all_urls.append(u)

        logger.info(
            f"🧾 TOTAL URLS: {len(all_urls)}"
        )

        # ---------------- DETAIL SCRAPING ----------------
        sem = asyncio.Semaphore(6)

        async def fetch_detail(i, url):

            async with sem:

                try:

                    html = await asyncio.wait_for(
                        client.get_html(url),
                        timeout=40
                    )

                    if not html:
                        return None

                    data = DetailParser.extract_data(
                        html,
                        url,
                        listing_type,
                        state,
                        listing_type
                    )

                    if not data:
                        return None

                    if i % 20 == 0:
                        logger.info(
                            f"📦 Progress: {i}/{len(all_urls)}"
                        )

                    return data

                except Exception as e:

                    logger.warning(
                        f"detail failed {url}: {str(e)[:80]}"
                    )

                    return None

        tasks = [
            fetch_detail(i, url)
            for i, url in enumerate(all_urls)
        ]

        raw_results = await asyncio.gather(*tasks)

        results = [
            r for r in raw_results
            if r
        ]

        results = deduplicate(results)

        timestamp = int(time.time())

        snapshot = {
            "created_at": timestamp,
            "listing_type": listing_type,
            "state": state,
            "count": len(results),
            "data": results
        }

        latest_file = (
            CACHE_DIR
            / f"latest_{listing_type}.json"
        )

        history_file = (
            HISTORY_DIR
            / f"{timestamp}_{listing_type}.json"
        )

        save_json(history_file, snapshot)
        save_json(latest_file, snapshot)

        cleanup_old_cache()

        logger.info(
            f"✅ Saved {len(results)} listings"
        )

        return results

    finally:
        await client.stop()