# 🏠 Hackathon Claude Scraper (Mudah Property Engine)

A Playwright-based async web scraper for extracting Malaysian property listings from Mudah.my with caching, deduplication, and structured parsing.

---

## 🚀 Features

- Async Playwright browser scraping
- Listing + detail page extraction
- Network interception for hidden property URLs
- Automatic scrolling for lazy-loaded content
- Price parsing (buy/rent separation)
- Image extraction with fallback filtering
- Bedroom / bathroom extraction
- Cache system (latest + history snapshots)
- TTL-based cache cleanup (3 days)
- Deduplication ("ghost" removal system)
- Batch scraping across multiple Malaysian states

---

## 📁 Project Structure
m-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
scraper/
├── browser/
│ └── playwright_client.py
├── parsers/
│ ├── listing_parser.py
│ └── detail_parser.py
├── storage/
│ └── csv_writer.py
├── utils/
├── sources/
│ └── mudah_config.py
engine.py
seed_all.py
cache/
## ⚙️ Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
2. Install Playwright browsers
python -m playwright install
▶️ How to Run
🔹 Run single state scrape (recommended for testing)
python -c "import asyncio; from scraper.engine import scrape_state; asyncio.run(scrape_state('johor'))"
🔹 Run full batch scrape (all states)
python seed_all.py
📦 Output Files

After running, results are stored in:

cache/
 ├── latest.json        # latest run snapshot
 ├── index.json         # pointer to latest file
 ├── history/
 │    ├── <timestamp>.json

Each snapshot contains:

{
  "created_at": 1234567890,
  "state": "johor",
  "count": 500,
  "data": [...]
}
🧠 Core Pipeline Flow
State → Category URLs → Listing URLs → Detail Pages → Parsed JSON → Cache
⚠️ Important Notes
1. Playwright is required

Run:

python -m playwright install
2. Expect occasional missing data ("ghost listings")

Some listings may have:

missing price
missing image
incomplete HTML rendering

This is normal due to dynamic website behavior.

3. Timeouts are expected

Mudah pages:

sometimes delay rendering
sometimes partially block scraping

Failures are handled safely and skipped.

4. Performance tuning

You can adjust:

concurrency:
MAX_CONCURRENCY
detail scraping load:
asyncio.Semaphore(6)
🧹 Cache System
TTL cleanup: 3 days
Auto deletes old JSON snapshots
Keeps latest snapshot always available
🧪 Debug Tips

If scraping seems stuck:

reduce concurrency
check Playwright install
ensure internet stability
run single state first (johor)
🛠 Recommended Next Improvements (optional)
JSON-LD extraction (for better price/image accuracy)
Retry system for failed listings
Proxy rotation (if scaling)
Database storage (PostgreSQL / MongoDB)
👨‍💻 Author Notes

This system is designed for:

hackathon-scale scraping
research / prototyping
property data aggregation pipelines

Not optimized for production anti-bot environments.


---

# 📌 CHECKLIST FOR YOUR FRIEND (IMPORTANT)

Give this to him exactly:

---

## ✅ SETUP CHECKLIST

### Environment
- [ ] Python 3.10+ installed
- [ ] Repo cloned correctly
- [ ] `pip install -r requirements.txt` run
- [ ] `python -m playwright install` run

---

## ⚙️ CODE CHECKS

### Playwright
- [ ] Ensure only ONE `finally: await page.close()` exists in `get_html`
- [ ] Confirm no duplicate cleanup blocks
- [ ] Ensure `domcontentloaded` is used (not `networkidle`)

---

### Engine
- [ ] `scrape_state()` runs without import errors
- [ ] Cache folder auto-creates:

cache/history/


---

### Parsers
- [ ] Listing parser returns valid URLs only
- [ ] Detail parser returns:
- title
- price_buy / price_rent
- image
- bedrooms/bathrooms

---

## 🧠 BEHAVIOR EXPECTATIONS

He should understand:

- ❗ Some listings will fail (normal)
- ❗ Some fields will be null (normal)
- ❗ Scraper is best-effort, not perfect

---

## 🚀 HOW TO TEST

### Step 1 (small test)
```bash
python -c "import asyncio; from scraper.engine import scrape_state; asyncio.run(scrape_state('johor'))"
Step 2 (full run)
python seed_all.py
🧹 DEBUG IF STUCK

If it hangs:

kill process
reduce concurrency to 4
restart Playwright install
rerun single state first
💀 KNOWN LIMITATIONS
No proxy rotation
Some anti-bot pages fail silently
Some images/prices require JS rendering delay
Some listings are partially blocked
Hackathon Claude3 — Malaysian Property Scraper

AI-ready Malaysian property scraping engine for:

Property sales
Property rentals
Live filtered searches
Cached nationwide scraping
Mudah.my integration
Async Playwright scraping

Built with:

Python
Playwright
AsyncIO
BeautifulSoup
Features
✅ Live Search Engine

Supports dynamic filters:

filters = {
    "location": "terengganu",
    "budget": 300000,
    "bedrooms": 2,
    "car_park": True,
    "listing_type": "sale"  # or "rent"
}

Supports:

sale listings
rent listings
budget filtering
bedrooms filtering
car park filtering
✅ Nationwide Scraper

Scrapes all Malaysian states and stores:

latest snapshots
historical snapshots
cached JSON results
✅ Intelligent Price Parsing

Automatically detects:

sale prices
rental prices

Rental keywords:

/month
monthly
sewa
rental

Logic:

rent listing → price_rent
sale listing → price_buy

Unified field:

"price": 2500
✅ Deduplication

Removes:

duplicate URLs
ghost listings
repeated entries
✅ Validation Layer

Filters out:

broken listings
junk prices
invalid URLs
malformed titles
Project Structure
scraper/
│
├── browser/
│   └── playwright_client.py
│
├── live/
│   └── live_search.py
│
├── parsers/
│   ├── detail_parser.py
│   └── listing_parser.py
│
├── utils/
│   ├── query_builder.py
│   ├── listing_validator.py
│   ├── price_cleaner.py
│   └── location_normalizer.py
│
├── engine.py
├── config.py
│
cache/
│
├── history/
├── latest_sale.json
├── latest_rent.json
└── index.json
Installation
1. Install Python packages
pip install -r requirements.txt
2. Install Playwright browsers
python -m playwright install
How To Use
1. Live Property Search

Run:

python test_live.py

Example:

filters = {
    "location": "johor",
    "budget": 2500,
    "bedrooms": 2,
    "car_park": True,
    "listing_type": "rent"
}

Returns:

JSON output
live scraped listings
filtered results
2. Scrape Entire Malaysia

Run:

python seed_all.py

This:

scrapes all states
saves JSON cache
updates latest snapshots
Important Architecture Notes
❗ Query Builder Is Now The Main Engine

Old:

mudah_config.py

New:

query_builder.py

The scraper now dynamically builds:

sale URLs
rental URLs
filter queries
pagination
URL Logic

Sale:

https://www.mudah.my/johor/properties-for-sale

Rent:

https://www.mudah.my/johor/properties-for-rent

Query Example:

?q=2+bedrooms,car+park
Cache System

Generated files:

cache/latest_sale.json
cache/latest_rent.json
cache/history/

Old cache auto-cleans after:

3 days
Important Files
test_live.py

Testing live property search.

seed_all.py

Nationwide scraper.

scraper/live/live_search.py

Main live search engine.

scraper/parsers/detail_parser.py

Extracts:

title
price
rent/sale detection
bedrooms
bathrooms
images
scraper/utils/query_builder.py

Builds dynamic Mudah URLs.

Common Problems
❌ await outside function

Wrong:

await something()

Correct:

asyncio.run(main())
❌ Playwright import errors

Install:

python -m playwright install
❌ Browser hangs forever

Cause:

wait_until="networkidle"

Fixed with:

wait_until="domcontentloaded"
Performance Notes

Current system:

async scraping
semaphore throttling
parallel detail scraping
timeout-safe fetching

Optimized for:

stability
anti-freeze
low RAM usage
Checklist For Integration
REQUIRED
1. Install dependencies
pip install -r requirements.txt
python -m playwright install
2. Verify imports work
python -c "from scraper.browser.playwright_client import PlaywrightClient; print('OK')"
3. Test live scraper
python test_live.py
4. Test nationwide scraper
python seed_all.py
Things To Watch Out For
⚠ Mudah Rate Limits

Too much concurrency may:

timeout
soft block
slow responses

Current safe concurrency:

Semaphore(6)
⚠ Rental Detection

Rental detection currently uses:

keywords
price thresholds

Future improvement:

ML classification
metadata extraction
⚠ Cache Size

History grows over time.

Auto cleanup:

3 day TTL
Future Improvements

Potential upgrades:

recommendation engine
FastAPI backend
vector search
embeddings
AI ranking
PostgreSQL storage
Redis caching
proxy rotation
CAPTCHA solving
image similarity search
Quick Start
git clone <repo>

cd Hackathon-claude3

pip install -r requirements.txt

python -m playwright install

python test_live.py
Example Output
{
  "title": "Apartment Austin Heights",
  "price": 2500,
  "price_rent": 2500,
  "listing_type": "rent",
  "bedrooms": 2,
  "bathrooms": 2,
  "location": "Johor Bahru"
}
