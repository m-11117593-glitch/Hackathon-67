import re
from typing import Dict, Any, Optional

def clean_price(price_str: str) -> Optional[float]:
    if not price_str:
        return None
    # Extract digits and decimal points
    cleaned = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None

def extract_number(text: str) -> Optional[int]:
    if not text:
        return None
    cleaned = re.sub(r'[^\d]', '', text)
    try:
        return int(cleaned) if cleaned else None
    except ValueError:
        return None

def normalize_state(state: str) -> str:
    if not state:
        return ""
    state = state.lower().replace(" ", "-")
    if "pinang" in state or "penang" in state:
        return "pulau-pinang"
    if "kl" in state or "kuala" in state:
        return "kuala-lumpur"
    if "sembilan" in state:
        return "negeri-sembilan"
    return state

def calculate_score(listing: Dict[str, Any]) -> int:
    """
    +2 complete listing
    +2 has image
    +1 valid price
    -2 missing key fields
    """
    score = 0
    key_fields = ["property_id", "title", "price", "location", "state", "url", "source"]
    
    # Check key fields missing
    missing_keys = sum(1 for k in key_fields if not listing.get(k))
    if missing_keys > 0:
        score -= 2
    else:
        # If no key fields missing and bedrooms/bathrooms exist, it's complete
        if listing.get("bedrooms") is not None and listing.get("bathrooms") is not None:
            score += 2

    if listing.get("image"):
        score += 2
        
    if listing.get("price") is not None and isinstance(listing.get("price"), (int, float)):
        score += 1
        
    return score
