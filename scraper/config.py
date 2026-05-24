import os

# Project structure
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
CACHE_FILE = os.path.join(CACHE_DIR, 'top50.json')

# Constraints
TARGET_LISTINGS_PER_STATE = 50
MAX_CONCURRENCY = 3
MAX_RETRIES = 2

# Headers for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
]

# States mapping (Standardized)
VALID_STATES = [
    "johor", "kedah", "kelantan", "melaka", "negeri-sembilan", 
    "pahang", "perak", "perlis", "pulau-pinang", "sabah", 
    "sarawak", "selangor", "terengganu", "kuala-lumpur", 
    "putrajaya", "labuan"
]
