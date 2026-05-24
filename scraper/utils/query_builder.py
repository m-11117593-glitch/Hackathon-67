from urllib.parse import quote_plus

from scraper.utils.location_normalizer import normalize_location


def calculate_price_range(budget: int):

    min_price = int(budget - (budget * 0.40))

    max_price = int(budget + (budget * 0.15))

    if min_price < 0:
        min_price = 0

    return min_price, max_price


def build_search_url(filters: dict) -> str:

    location = filters.get("location", "malaysia")

    budget = filters.get("budget")

    bedrooms = filters.get("bedrooms")

    car_park = filters.get("car_park", False)

    normalized_location = normalize_location(location)

    base_url = f"https://www.mudah.my/{normalized_location}/properties-for-sale"

    params = []

    # ---------------- PRICE ----------------
    if budget:

        min_price, max_price = calculate_price_range(budget)

        params.append(
            f"price={min_price}-{max_price}"
        )

    # ---------------- SEARCH QUERY ----------------
    q_parts = []

    if bedrooms:
        q_parts.append(f"{bedrooms} bedrooms")

    if car_park:
        q_parts.append("car park")

    if q_parts:

        q = ",".join(q_parts)

        params.append(
            f"q={quote_plus(q)}"
        )

    # ---------------- FINAL URL ----------------
    if params:
        return base_url + "?" + "&".join(params)

    return base_url