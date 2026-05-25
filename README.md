# 🏠 Mudah Property Scraper (Live + Batch Engine)

A high-performance **Playwright-based property scraping system** for Mudah.my that supports:

- 🏡 Sale + Rent listings
- ⚡ Live search mode (fast, capped at 50 results)
- 📦 Batch scraping across Malaysian states
- 🧠 Fallback query strategy (smart search variants)
- 🖼️ Listing + full detail scraping (including description)
- 💾 JSON caching for downstream ML / LLM usage

---

# 🚀 Quick Start

## 1. Install dependencies

```bash
pip install playwright bs4 pandas
playwright install
2. Run LIVE search (recommended test)
python test_live.py
Example filters:
filters = {
    "location": "johor",
    "budget": 300000,
    "bedrooms": 2,
    "car_park": True,
    "listing_type": "rent"   # OR "sale"
}
3. Run FULL batch scraping (all states)
python seed_all.py

This will:

Loop through all states in VALID_STATES
Scrape listings per category
Save JSON snapshots in /cache/history/
⚙️ Core Features
🏡 Listing Types

Supported:

"sale" → properties-for-sale
"rent" → properties-for-rent

Automatically affects:

URL routing
Price mapping (price_buy vs price_rent)
JSON output structure
📊 Output Format (IMPORTANT)

Each property looks like:

{
  "property_id": "uuid",
  "title": "Fully Furnished Condo",
  "price": 1200,
  "price_buy": null,
  "price_rent": 1200,
  "listing_type": "rent",
  "location": "Johor Bahru",
  "state": "johor",
  "bedrooms": 2,
  "bathrooms": 1,
  "image": "https://...",
  "description": "Full listing description text...",
  "url": "https://www.mudah.my/...",
  "source": "live_search"
}
🔍 How LIVE search works
Function:
live_property_search(filters)
Flow:
Generates fallback query variants
Builds search URLs
Scrapes listing pages
Extracts property URLs
Limits results to top 50
Scrapes full property pages
Extracts:
Title
Price
Bedrooms / Bathrooms
Images
FULL DESCRIPTION (Playwright expanded)
Saves JSON to /scraper/temp/
🧠 Query System (IMPORTANT)

File:

scraper/utils/query_builder.py

Responsible for:

Price range filtering
Bedroom filters
Car park filtering
Location normalization

Example:

build_search_url({
    "location": "johor",
    "budget": 300000,
    "bedrooms": 2,
    "car_park": True
})
🔄 Fallback System

File:

scraper/live/search_fallback.py

It automatically generates:

Strict search
Remove car park filter
Remove bedroom filter
Broad search (budget expanded)

This improves hit rate when listings are sparse.

⚡ Performance Rules
Hard limits:
Max results per live search: 50
Max pages per variant: 2
Concurrent scraping: 6 tasks
Browser concurrency: controlled via semaphore
🧱 Core Modules
1. Playwright Client

File:

scraper/browser/playwright_client.py

Responsible for:

Browser lifecycle
Anti-bot delay
Page scrolling
"Show More" expansion
HTML extraction
2. Listing Parser

File:

scraper/parsers/listing_parser.py

Extracts:

Valid property URLs only
Filters ads, images, agents, spam links
Deduplicates links
3. Detail Parser

File:

scraper/parsers/detail_parser.py

Extracts:

Title
Price
Location
Images
Bedrooms / bathrooms
FULL DESCRIPTION (important feature)
4. Live Engine

File:

scraper/live/live_search.py

Main entry point:

await live_property_search(filters)
5. Batch Engine

File:

scraper/engine.py

Used for:

full state scraping
cached dataset generation
historical snapshots
💾 Cache System
Live search:
scraper/temp/live_search_<uuid>.json
Batch mode:
cache/latest_sale.json
cache/latest_rent.json
cache/history/<timestamp>.json
⚠️ Important Notes
1. Description extraction
Uses full listing page
Automatically clicks "Show More"
Removes UI buttons from text
2. Listing type logic
sale → price_buy
rent → price_rent
unified field: price
3. Top 50 rule

Hard enforced:

unique_urls[:50]
4. Anti-bot behavior
Random user agent
Random sleep delay
Domain semaphores
Scroll simulation
🧪 Testing
Quick test
python test_live.py
Full system test
python seed_all.py
🔥 Recommended Workflow
Run test_live.py
Validate JSON output
Check description quality
Run seed_all.py (single state first)
Scale to all states
🚀 System Status

✔ Live search working
✔ Rent + Sale supported
✔ Description extraction fixed
✔ Show-more automation added
✔ Top-50 enforced
✔ Fallback search engine active
✔ JSON caching system stable

🧠 Future Upgrade Ideas (optional)
Ranking system (best deal scoring)
AI summarizer for descriptions
Duplicate spam filtering (agent detection)
Vector DB for property search
Frontend API wrapper (FastAPI)
👨‍💻 End

This system is now production-ready for:

datasets
AI agents
property recommendation engines
hackathon demos
