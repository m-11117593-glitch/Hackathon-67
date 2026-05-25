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
