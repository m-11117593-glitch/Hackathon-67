from urllib.parse import quote_plus

from scraper.utils.location_normalizer import normalize_location


def calculate_price_range(
    budget: int,
    listing_type: str = "sale"
):

    # ---------------- RENT ----------------
    if listing_type == "rent":

        min_price = int(budget - (budget * 0.40))
        max_price = int(budget + (budget * 0.20))

    # ---------------- SALE ----------------
    else:

        min_price = int(budget - (budget * 0.40))
        max_price = int(budget + (budget * 0.15))

    if min_price < 0:
        min_price = 0

    return min_price, max_price


def build_search_url(
    filters: dict,
    page: int = 1
) -> str:

    location = filters.get("location", "malaysia")

    listing_type = filters.get(
        "listing_type",
        "sale"
    )

    budget = filters.get("budget")

    bedrooms = filters.get("bedrooms")

    car_park = filters.get(
        "car_park",
        False
    )

    normalized_location = normalize_location(location)

    # ---------------- SALE / RENT ----------------
    if listing_type == "rent":
        base_url = (
            f"https://www.mudah.my/"
            f"{normalized_location}/properties-for-rent"
        )
    else:
        base_url = (
            f"https://www.mudah.my/"
            f"{normalized_location}/properties-for-sale"
        )

    params = []

    # ---------------- PAGE ----------------
    params.append(f"o={page}")

    # ---------------- PRICE ----------------
    if budget:

        min_price, max_price = calculate_price_range(
            budget,
            listing_type
        )

        params.append(
            f"price={min_price}-{max_price}"
        )

    # ---------------- QUERY ----------------
    q_parts = []

    if bedrooms:
        q_parts.append(f"{bedrooms} bedroom")

    if car_park:
        q_parts.append("carpark")

    if q_parts:

        q = ",".join(q_parts)

        params.append(
            f"q={quote_plus(q)}"
        )

    return base_url + "?" + "&".join(params)