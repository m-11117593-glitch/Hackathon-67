from bs4 import BeautifulSoup
from typing import Dict, Any
import uuid
import re

from scraper.utils.price_cleaner import clean_price


class DetailParser:

    @staticmethod
    def extract_data(html: str, url: str, source: str, state: str, listing_type: str = "sale") -> Dict[str, Any]:

        soup = BeautifulSoup(html, "html.parser")

        data = {
            "property_id": str(uuid.uuid4()),
            "title": None,
            "price": None,
            "price_buy": None,
            "price_rent": None,
            "listing_type": listing_type,
            "location": None,
            "state": state,
            "bedrooms": None,
            "bathrooms": None,
            "image": None,
            "description": None,
            "url": url,
            "source": source
        }

        # TITLE
        h1 = soup.find("h1")
        if h1:
            data["title"] = h1.get_text(strip=True)

        if not data["title"]:
            og = soup.find("meta", property="og:title")
            if og:
                data["title"] = og.get("content")

        # PRICE
        price_el = soup.select_one('[data-testid="ad-price"]')

        if price_el:
            cleaned = clean_price(price_el.get_text(strip=True))
            if cleaned:
                data["price"] = cleaned
                if listing_type == "rent":
                    data["price_rent"] = cleaned
                else:
                    data["price_buy"] = cleaned

        # IMAGES
        images = []

        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src")

            if not src:
                continue

            if any(x in src.lower() for x in ["logo", "icon", "avatar", "placeholder"]):
                continue

            if "cdn.rnudah.com" in src:
                images.insert(0, src)
            elif src.startswith("http"):
                images.append(src)

        if images:
            data["image"] = images[0]

        # BED / BATH
        text = soup.get_text(" ", strip=True).lower()

        beds = re.search(r"(\d+)\s*(bed|bedroom|bedrooms)", text)
        if beds:
            data["bedrooms"] = int(beds.group(1))

        baths = re.search(r"(\d+)\s*(bath|bathroom|bathrooms)", text)
        if baths:
            data["bathrooms"] = int(baths.group(1))

        # LOCATION
        meta = soup.find("meta", {"name": "keywords"})
        if meta:
            data["location"] = meta.get("content", "").split(",")[0]
        else:
            data["location"] = state.capitalize()

        # DESCRIPTION
        desc = soup.select_one("#property-adview-description")

        if desc:
            for btn in desc.select("button"):
                btn.decompose()

            text_desc = desc.get_text("\n", strip=True)
            text_desc = re.sub(r"\n{2,}", "\n", text_desc)
            data["description"] = text_desc

        return data