import asyncio
import json
from pprint import pprint

from scraper.live.live_search import live_property_search


async def run_test(name: str, filters: dict):

    print("\n" + "=" * 80)
    print(f"TEST: {name}")
    print("=" * 80)

    print("\nFILTERS:")
    pprint(filters)

    try:
        results = await live_property_search(filters)

        print("\n" + "-" * 80)
        print("RESULT SUMMARY")
        print("-" * 80)

        print(f"Total Results : {results.get('total_results', 0)}")
        print(f"JSON Path     : {results.get('json_path')}")

        listings = results.get("results", [])

        if not listings:
            print("\n❌ NO RESULTS FOUND")
            return

        print(f"\n✅ Showing first {min(5, len(listings))} results:\n")

        for i, item in enumerate(listings[:5], start=1):

            print("=" * 80)
            print(f"RESULT #{i}")
            print("=" * 80)

            print(f"Title         : {item.get('title')}")
            print(f"Price         : {item.get('price')}")
            print(f"Listing Type  : {item.get('listing_type')}")
            print(f"Bedrooms      : {item.get('bedrooms')}")
            print(f"Bathrooms     : {item.get('bathrooms')}")
            print(f"Location      : {item.get('location')}")
            print(f"State         : {item.get('state')}")
            print(f"URL           : {item.get('url')}")
            print(f"Image         : {item.get('image')}")

            print()

        print("-" * 80)
        print("RAW JSON PREVIEW")
        print("-" * 80)

        print(json.dumps(listings[0], indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")


async def main():

    # ---------------------------------------------------
    # SALE TEST
    # ---------------------------------------------------
    sale_filters = {
        "location": "terengganu",
        "budget": 300000,
        "bedrooms": 1,
        "car_park": True,
        "listing_type": "sale"
    }

    # ---------------------------------------------------
    # RENT TEST
    # ---------------------------------------------------
    rent_filters = {
        "location": "johor",
        "budget": 1500,
        "bedrooms": 2,
        "car_park": True,
        "listing_type": "rent"
    }

    await run_test("SALE SEARCH", sale_filters)

    await asyncio.sleep(3)

    await run_test("RENT SEARCH", rent_filters)


if __name__ == "__main__":
    asyncio.run(main())