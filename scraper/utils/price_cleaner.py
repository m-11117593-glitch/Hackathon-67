import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def clean_price(value):
    """
    Cleans raw RM price strings into float.

    RULES:
    - NEVER modify price meaning (no math, no conversion)
    - Only extract numeric value
    - Reject impossible values
    """

    if value is None or pd.isna(value):
        return None

    if not isinstance(value, str):
        value = str(value)

    # remove spaces + normalize
    text = value.replace(",", "").strip().lower()

    # extract number (supports 1.2m, 120k, etc)
    match = re.search(r"(\d+(\.\d+)?)(\s*[mk])?", text)

    if not match:
        return None

    number = float(match.group(1))
    suffix = match.group(3)

    # handle K / M properly (ONLY for normalization, not transformation of meaning)
    if suffix:
        suffix = suffix.strip()
        if suffix == "k":
            number *= 1_000
        elif suffix == "m":
            number *= 1_000_000

    # HARD FILTER: remove junk values
    if number <= 500:
        return None

    if number >= 100_000_000:
        return None

    return number