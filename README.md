🏠 Mudah Property Scraper (AI Dataset Builder)

A high-performance asynchronous web scraper that collects real estate listings from Mudah.my, designed to generate structured datasets for AI systems, recommendation engines, or LLM pipelines.

It supports:

🏡 Sale & Rent properties
📍 State-by-state scraping (Malaysia)
⚡ Concurrent Playwright scraping
🧠 Clean JSON output for AI/LLM usage
📦 Automatic caching + history tracking
🔍 Top 50 listings per state (optimized for LLM ingestion)
🚀 Features
✔ Full property listing extraction (title, price, location, images, bedrooms, bathrooms)
✔ Deep scraping of individual listing pages (full description included)
✔ Smart filtering (removes invalid/bad listings)
✔ Top 50 dataset cap (LLM-safe)
✔ State-separated storage system
✔ Rent + Sale classification
✔ Automatic deduplication
✔ Retry + concurrency control
📦 Output Structure (IMPORTANT)

After running, data is stored like this:

cache/
  johor/
    latest/
      sale.json
      rent.json

    history/
      1712345678_sale.json
      1712349999_rent.json

  selangor/
    latest/
      sale.json
      rent.json

    history/
      ...
🧠 What Each File Means
📌 latest/

Always contains the most recent dataset per state + listing type

Example:

cache/johor/latest/sale.json

✔ Used for AI inference
✔ Always overwritten (latest snapshot)

📌 history/

Stores all past snapshots (timestamped)

Example:

cache/johor/history/1712345678_sale.json

✔ Used for backup
✔ Dataset versioning
✔ Training / analytics

⚙️ Main Function (Simple Integration)
✅ One-line usage
from scraper.engine import scrape_properties
🚀 Example Call
import asyncio
from scraper.engine import scrape_properties

async def main():

    results = await scrape_properties({
        "location": "johor",
        "listing_type": "sale",   # or "rent"
        "budget": 300000,
        "bedrooms": 2,
        "car_park": True
    })

    print("TOTAL:", len(results))
    print(results[0])

asyncio.run(main())
🧩 Filter Options
Field	Type	Description
location	str	State in Malaysia (johor, selangor, etc.)
listing_type	str	"sale" or "rent"
budget	int	Target price range
bedrooms	int	Number of bedrooms
car_park	bool	Include car park filter
🧠 How Pricing Works

The system automatically converts budget into a realistic range:

min_price = budget - 40%
max_price = budget + 15%

Example:

budget = 300000

min = 180000
max = 345000
🏗 Architecture Overview
seed_all.py
   ↓
scrape_properties()
   ↓
PlaywrightClient (browser)
   ↓
ListingParser (extract URLs)
   ↓
DetailParser (extract full property data)
   ↓
Validation + Deduplication
   ↓
JSON Storage (state-based)
⚡ Performance Design
Async scraping (Playwright)
Semaphore-controlled concurrency (safe crawling)
Domain-aware request throttling
Auto retry + timeout protection
Top-50 cap for LLM optimization
🧹 Data Cleaning Rules

✔ Invalid listings removed
✔ Duplicate URLs removed
✔ Price noise filtered
✔ Broken links ignored

🧠 For AI / LLM Usage

This scraper is optimized for:

🧾 RAG systems
🏡 property recommendation models
📊 dataset training
🤖 agent-based real estate systems

Each listing includes:

{
  "title": "...",
  "price": 300000,
  "price_buy": 300000,
  "price_rent": null,
  "location": "Johor Bahru",
  "bedrooms": 3,
  "bathrooms": 2,
  "image": "...",
  "url": "...",
  "state": "johor"
}
🔥 Seed Full Dataset (ALL STATES)
from scraper.seed_all import main
import asyncio

asyncio.run(main())

This will:

loop all Malaysian states
scrape sale + rent
store structured datasets per state
🧪 Testing
python test_live.py

or

python seed_all.py
📌 Key Design Upgrade (IMPORTANT)
Before:
Overwriting single latest file ❌
Mixed state data ❌
Now:
Fully isolated per state ✔
Separate rent/sale datasets ✔
Versioned history ✔
LLM-ready structure ✔
🚀 Future Expansion Ideas
Vector search over listings (semantic matching)
AI property recommendation agent
FastAPI backend wrapper
Real-time scraping API endpoint
