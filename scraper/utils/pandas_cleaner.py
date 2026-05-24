import pandas as pd
import logging

logger = logging.getLogger(__name__)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting pandas normalization (NO FILTERING MODE)...")

    # -----------------------------
    # REMOVE DUPLICATES ONLY
    # -----------------------------
    if "url" in df.columns:
        df = df.drop_duplicates(subset=["url"])

    # -----------------------------
    # TITLE (JUST FILL MISSING)
    # -----------------------------
    if "title" in df.columns:
        df["title"] = df["title"].fillna("Unknown")

    # -----------------------------
    # PRICE NORMALIZATION ONLY
    # -----------------------------
    for col in ["price", "price_buy", "price_rent"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # -----------------------------
    # BEDROOMS / BATHROOMS NORMALIZATION
    # -----------------------------
    if "bedrooms" in df.columns:
        df["bedrooms"] = pd.to_numeric(df["bedrooms"], errors="coerce")

    if "bathrooms" in df.columns:
        df["bathrooms"] = pd.to_numeric(df["bathrooms"], errors="coerce")

    # -----------------------------
    # LOCATION FIX ONLY (NO DROPPING)
    # -----------------------------
    if "location" in df.columns and "state" in df.columns:
        df["location"] = df["location"].fillna(df["state"])

    # -----------------------------
    # URL SAFETY (DO NOT FILTER HARD)
    # -----------------------------
    if "url" in df.columns:
        df["url"] = df["url"].fillna("")

    # -----------------------------
    # SORT ONLY (SAFE)
    # -----------------------------
    if "price" in df.columns:
        df = df.sort_values(by="price", ascending=False, na_position="last")

    logger.info(f"Normalized dataframe size: {len(df)}")

    return df