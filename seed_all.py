import asyncio
import logging
from scraper.config import VALID_STATES
from scraper.engine import scrape_state

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting batch scrape for all states...")

    for state in VALID_STATES:
        logger.info(f"--- Scraping State: {state} ---")

        try:
            await scrape_state(state)

        except Exception as e:
            logger.error(f"Failed {state}: {e}")

        # ✅ IMPORTANT: prevents browser / rate stress
        await asyncio.sleep(2)

    logger.info("Batch scrape completed.")


if __name__ == "__main__":
    asyncio.run(main())