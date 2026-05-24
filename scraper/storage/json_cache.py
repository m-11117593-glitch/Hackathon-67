import os
import json
import logging
from typing import List, Dict, Any
from scraper.config import CACHE_DIR, CACHE_FILE
from scraper.utils.normalize import calculate_score

logger = logging.getLogger(__name__)

def save_top50_json(listings: List[Dict[str, Any]]) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Score and sort listings
    scored_listings = [(calculate_score(item), item) for item in listings]
    scored_listings.sort(key=lambda x: x[0], reverse=True)
    
    # We must have EXACTLY 50 listings if possible (handled in engine.py by merging CSV)
    # This just writes what it receives, up to 50
    best_listings = [item for score, item in scored_listings[:50]]
    
    try:
        with open(CACHE_FILE, mode='w', encoding='utf-8') as f:
            json.dump(best_listings, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(best_listings)} listings to {CACHE_FILE}")
    except Exception as e:
        logger.error(f"Failed to save JSON cache: {e}")
