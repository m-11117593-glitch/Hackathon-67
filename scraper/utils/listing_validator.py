# scraper/utils/listing_validator.py

from typing import List, Dict, Any
import re


class ListingValidator:
    """
    Filters and validates scraped property listings
    before saving to JSON / CSV.
    """

    @staticmethod
    def is_valid_url(url: str) -> bool:
        if not url:
            return False

        # Must look like a real property listing
        patterns = [
            r"/\d+\.htm",              # real Mudah listing pages
            r"/property/",            # some property endpoints
            r"-\d{6,}$",              # listing ID at end
        ]

        return any(re.search(p, url) for p in patterns)


    @staticmethod
    def is_valid_title(title: str) -> bool:
        if not title:
            return False

        title = title.lower().strip()

        # reject junk titles
        bad_titles = [
            "www.mudah.my",
            "mudah.my",
            "loading",
            "untitled",
            "property",
        ]

        if title in bad_titles:
            return False

        # must be descriptive enough
        return len(title) > 5


    @staticmethod
    def is_valid_price(
        price: Any,
        listing_type: str = "sale"
    ) -> bool:

        if price is None:
            return True

        try:

            price = float(price)

            # ---------------- RENT ----------------
            if listing_type == "rent":

                return (
                    price > 100
                    and price < 30000
                )

            # ---------------- SALE ----------------
            return price > 10000

        except:
            return False


    @staticmethod
    def is_valid_listing(listing: Dict[str, Any]) -> bool:
        """
        Main validation rule
        """

        url = listing.get("url")
        title = listing.get("title")
        price = listing.get("price")

        # MUST pass at least URL + title sanity
        if not ListingValidator.is_valid_url(url):
            return False

        if not ListingValidator.is_valid_title(title):
            return False

        if not ListingValidator.is_valid_price(price):
            return False

        return True


    @staticmethod
    def filter_listings(listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove invalid listings safely
        """

        cleaned = []

        for l in listings:
            if ListingValidator.is_valid_listing(l):
                cleaned.append(l)

        return cleaned