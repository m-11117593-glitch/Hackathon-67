import asyncio

from scraper.live.live_search import live_property_search


async def main():

    filters = {
        "location": "terengganu",
        "budget": 300000,
        "bedrooms": 1,
        "car_park": True
    }

    results = await live_property_search(filters)

    print(f"\nTOTAL RESULTS: {results['total_results']}")

    print(f"\nJSON PATH: {results['json_path']}")

    if results["results"]:

        print("\nFIRST RESULT:\n")

        print(results["results"][0])


if __name__ == "__main__":
    asyncio.run(main())