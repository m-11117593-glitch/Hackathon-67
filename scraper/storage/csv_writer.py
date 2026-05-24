import os
import csv
import logging
from typing import List, Dict, Any

import pandas as pd

from scraper.config import DATA_DIR
from scraper.utils.normalize import calculate_score
from scraper.utils.pandas_cleaner import clean_dataframe

logger = logging.getLogger(__name__)


FIELDNAMES = [
    "property_id",

    "title",

    # MAIN ranking price
    "price",

    # detailed prices
    "price_buy",
    "price_rent",

    "location",
    "state",

    "bedrooms",
    "bathrooms",

    "image",

    "url",
    "source"
]


def save_to_csv(
    state: str,
    listings: List[Dict[str, Any]]
) -> None:

    os.makedirs(DATA_DIR, exist_ok=True)

    filepath = os.path.join(
        DATA_DIR,
        f"{state}.csv"
    )

    # -----------------------------------
    # EMPTY EXPORT
    # -----------------------------------
    if not listings:

        logger.warning(f"No listings for {state}")

        with open(
            filepath,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=FIELDNAMES
            )

            writer.writeheader()

        return

    # -----------------------------------
    # SCORE LISTINGS
    # -----------------------------------
    scored = []

    for item in listings:

        try:
            score = calculate_score(item)
            scored.append((score, item))

        except Exception as e:
            logger.warning(f"Score failed: {e}")

    # sort highest score first
    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    best_listings = [
        item for score, item in scored
    ]

    # -----------------------------------
    # CONVERT TO DATAFRAME
    # -----------------------------------
    try:

        df = pd.DataFrame(best_listings)

        logger.info(
            f"Raw dataframe size: {len(df)}"
        )

        # -----------------------------------
        # CLEAN DATAFRAME
        # -----------------------------------
        df = clean_dataframe(df)

        logger.info(
            f"Cleaned dataframe size: {len(df)}"
        )

        # -----------------------------------
        # ENSURE FIELD ORDER
        # -----------------------------------
        for field in FIELDNAMES:

            if field not in df.columns:
                df[field] = None

        df = df[FIELDNAMES]

        # -----------------------------------
        # EXPORT CSV
        # -----------------------------------
        df.to_csv(
            filepath,
            index=False,
            encoding="utf-8"
        )

        logger.info(
            f"Saved cleaned CSV → {filepath}"
        )

    except Exception as e:

        logger.error(
            f"CSV save failed: {e}"
        )


def load_from_csv(
    state: str
) -> List[Dict[str, Any]]:

    filepath = os.path.join(
        DATA_DIR,
        f"{state}.csv"
    )

    if not os.path.exists(filepath):
        return []

    try:

        df = pd.read_csv(filepath)

        # convert NaN → None
        df = df.where(
            pd.notnull(df),
            None
        )

        return df.to_dict("records")

    except Exception as e:

        logger.error(
            f"CSV load failed: {e}"
        )

        return []