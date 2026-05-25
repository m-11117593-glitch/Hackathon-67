from bs4 import BeautifulSoup
from typing import Dict, Any
import uuid
import re

from scraper.utils.price_cleaner import clean_price


class DetailParser:

    @staticmethod
    def extract_data(
        html: str,
        url: str,
        source: str,
        state: str,
        listing_type: str
    ) -> Dict[str, Any]:

        soup = BeautifulSoup(html, "html.parser")

        data = {
            "property_id": str(uuid.uuid4()),
            "title": None,
            "price": None,
            "listing_type": listing_type,
            "location": None,
            "state": state,
            "bedrooms": None,
            "bathrooms": None,
            "image": None,
            "url": url,
            "source": source
        }

        # ---------------- TITLE ----------------
        h1 = soup.find("h1")

        if h1:
            data["title"] = h1.get_text(strip=True)

        if not data["title"]:
            og = soup.find(
                "meta",
                property="og:title"
            )

            if og:
                data["title"] = og.get("content")

        # ---------------- PRICE ----------------
        price_el = soup.select_one(
            '[data-testid="ad-price"]'
        )

        if price_el:

            cleaned = clean_price(
                price_el.get_text(strip=True)
            )

            if cleaned:
                data["price"] = cleaned

        # fallback
        if not data["price"]:

            raw_prices = []

            for p in soup.find_all(string=True):

                if p and "RM" in p:

                    cleaned = clean_price(p)

                    if cleaned:
                        raw_prices.append(cleaned)

            if raw_prices:

                raw_prices.sort()

                if listing_type == "rent":
                    data["price"] = raw_prices[0]
                else:
                    data["price"] = raw_prices[-1]

        # ---------------- IMAGE ----------------
        images = []

        for img in soup.find_all("img"):

            src = (
                img.get("src")
                or img.get("data-src")
            )

            if not src:
                continue

            src_lower = src.lower()

            if any(
                x in src_lower
                for x in [
                    "logo",
                    "icon",
                    "avatar",
                    "placeholder"
                ]
            ):
                continue

            if "cdn.rnudah.com" in src:
                images.insert(0, src)

            elif src.startswith("http"):
                images.append(src)

        if images:
            data["image"] = images[0]

        # ---------------- TEXT ----------------
        text = soup.get_text(
            " ",
            strip=True
        ).lower()

        # ---------------- RENT DETECTION ----------------
        if listing_type == "rent":

            rent_keywords = [
                "/month",
                "monthly",
                "sewa",
                "rental"
            ]

            has_rent_keyword = any(
                k in text
                for k in rent_keywords
            )

            # reject fake rent listings
            if data["price"]:

                if (
                    data["price"] > 30000
                    and not has_rent_keyword
                ):
                    return None

        # ---------------- BEDROOMS ----------------
        beds = re.search(
            r"(\d+)\s*(bed|bedroom|bedrooms)",
            text
        )

        if beds:
            data["bedrooms"] = int(
                beds.group(1)
            )

        # ---------------- BATHROOMS ----------------
        baths = re.search(
            r"(\d+)\s*(bath|bathroom|bathrooms)",
            text
        )

        if baths:
            data["bathrooms"] = int(
                baths.group(1)
            )

        # ---------------- LOCATION ----------------
        meta = soup.find(
            "meta",
            {"name": "keywords"}
        )

        if meta:

            data["location"] = (
                meta.get("content", "")
                .split(",")[0]
            )

        else:
            data["location"] = state.capitalize()

        return data