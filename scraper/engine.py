import asyncio
import logging
import json
import os
import time
from pathlib import Path

from scraper.browser.playwright_client import PlaywrightClient
from scraper.sources.mudah_config import MUDAH_CATEGORIES
from scraper.parsers.listing_parser import ListingParser
from scraper.parsers.detail_parser import DetailParser

logger = logging.getLogger(__name__)

CACHE_DIR = Path("cache")
HISTORY_DIR = CACHE_DIR / "history"
LATEST_FILE = CACHE_DIR / "latest.json"
INDEX_FILE = CACHE_DIR / "index.json"

TTL_SECONDS = 60 * 60 * 24 * 3  # 3 days


def ensure_dirs():
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cleanup_old_cache():
    now = time.time()

    for file in HISTORY_DIR.glob("*.json"):
        try:
            ts = float(file.stem)
            if now - ts > TTL_SECONDS:
                file.unlink()
                logger.info(f"🧹 Deleted old cache: {file.name}")
        except Exception:
            continue


def deduplicate(listings):
    seen = set()
    clean = []

    for item in listings:
        key = item.get("property_id") or item.get("url")

        if not key or key in seen:
            continue

        seen.add(key)
        clean.append(item)

    return clean


async def scrape_state(state: str):

    ensure_dirs()

    client = PlaywrightClient()
    await client.start()

    try:
        logger.info(f"🚀 Scraping Mudah (v3 FIXED): {state}")

        all_listings = []
        seen_urls = set()

        # -----------------------------
        # LISTING SCRAPING
        # -----------------------------
        for cat in MUDAH_CATEGORIES:

            logger.info(f"📦 Category: {cat.name}")

            category_urls = []

            for page in range(1, cat.max_pages + 1):

                try:
                    url = cat.url_builder(state, page)
                    html = await client.get_html(url)

                    if not html or len(html) < 500:
                        break

                    urls = ListingParser.extract_urls(html, cat.name)

                    if not urls:
                        break

                    new_count = 0

                    for u in urls:
                        if u not in seen_urls:
                            seen_urls.add(u)
                            category_urls.append(u)
                            new_count += 1

                    if new_count == 0:
                        break

                except Exception as e:
                    logger.warning(f"{cat.name} page {page} failed: {e}")
                    break

            for u in category_urls:
                all_listings.append((cat.name, u))

        logger.info(f"🧾 TOTAL LISTINGS: {len(all_listings)}")

        # -----------------------------
        # DETAIL SCRAPING (FIXED: PARALLEL + TIMEOUT SAFE)
        # -----------------------------

        results = []
        sem = asyncio.Semaphore(6)  # slightly lower = more stable

        async def fetch_detail(i, source, url):

            async with sem:
                try:
                    html = await asyncio.wait_for(
                        client.get_html(url),
                        timeout=40
                    )

                    if not html:
                        return None

                    data = DetailParser.extract_data(html, url, source, state)

                    if i % 50 == 0:
                        logger.info(f"📦 Progress: {i}/{len(all_listings)}")

                    return data

                except Exception as e:
                    logger.warning(f"detail failed {url}: {str(e)[:80]}")
                    return None

        tasks = [
            fetch_detail(i, source, url)
            for i, (source, url) in enumerate(all_listings)
        ]

        raw_results = await asyncio.gather(*tasks)

        results = [r for r in raw_results if r]

        # -----------------------------
        # DEDUPLICATION
        # -----------------------------
        results = deduplicate(results)

        # -----------------------------
        # CACHE STORAGE
        # -----------------------------
        timestamp = int(time.time())

        snapshot = {
            "created_at": timestamp,
            "state": state,
            "count": len(results),
            "data": results
        }

        history_file = HISTORY_DIR / f"{timestamp}.json"
        save_json(history_file, snapshot)
        save_json(LATEST_FILE, snapshot)

        save_json(INDEX_FILE, {
            "latest_file": str(history_file),
            "latest_timestamp": timestamp,
            "state": state,
            "count": len(results)
        })

        cleanup_old_cache()

        logger.info(f"✅ Saved {len(results)} listings for {state}")

    finally:
        await client.stop()