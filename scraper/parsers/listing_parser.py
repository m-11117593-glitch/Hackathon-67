from bs4 import BeautifulSoup
from typing import List
import re


class ListingParser:

    @staticmethod
    def extract_urls(html: str, source: str) -> List[str]:

        soup = BeautifulSoup(html, "html.parser")

        urls = []

        seen = set()

        for a in soup.select("a[href]"):

            href = a.get("href")

            if not href:
                continue

            href = href.strip()

            # ---------------- ABSOLUTE URL ----------------
            if href.startswith("/"):
                href = "https://www.mudah.my" + href

            # ---------------- MUST BE MUDAH ----------------
            if not href.startswith("https://www.mudah.my"):
                continue

            href_lower = href.lower()

            # ---------------- REMOVE BAD LINKS ----------------
            bad_keywords = [
                "facebook",
                "twitter",
                "instagram",
                "banner",
                "ads",
                "tracking",
                "login",
                "signup",
                "register",
                "directory",
                "agent",
                "contact",
                "help",
                "faq",
                ".svg",
                ".png",
                ".jpg",
                ".jpeg"
            ]

            if any(x in href_lower for x in bad_keywords):
                continue

            # ---------------- REMOVE BROKEN HTML ----------------
            if "<" in href or ">" in href:
                continue

            # ---------------- STRICT PROPERTY VALIDATION ----------------
            valid = False

            valid_patterns = [

                # MOST COMMON
                r"/property/properties-in-",

                # .htm listings
                r"/[\w\-]+-\d+\.htm",

                # numeric property ids
                r"/property/[\w\-]+"
            ]

            for pattern in valid_patterns:

                if re.search(pattern, href_lower):
                    valid = True
                    break

            if not valid:
                continue

            # ---------------- REMOVE FAKE PROPERTY PAGES ----------------
            fake_pages = [
                "/property/apartment",
                "/property/condominium",
                "/property/house",
                "/property/bungalow",
                "/property/terrace",
            ]

            if any(x in href_lower for x in fake_pages):
                continue

            # ---------------- DEDUPE ----------------
            if href in seen:
                continue

            seen.add(href)

            urls.append(href)

        return urls