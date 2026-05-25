import asyncio
import logging

from scraper.config import VALID_STATES
from scraper.engine import scrape_properties

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def main():

    logger.info(
        "Starting batch scrape..."
    )

    for state in VALID_STATES:

        logger.info(
            f"--- SALE: {state} ---"
        )

        try:

            await scrape_properties({
                "location": state,
                "listing_type": "sale"
            })

        except Exception as e:

            logger.error(
                f"SALE failed {state}: {e}"
            )

        await asyncio.sleep(2)

        logger.info(
            f"--- RENT: {state} ---"
        )

        try:

            await scrape_properties({
                "location": state,
                "listing_type": "rent"
            })

        except Exception as e:

            logger.error(
                f"RENT failed {state}: {e}"
            )

        await asyncio.sleep(2)

    logger.info(
        "Batch scrape completed."
    )


if __name__ == "__main__":
    asyncio.run(main())