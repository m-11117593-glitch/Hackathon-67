import json
import os
import time
import uuid


TEMP_DIR = "scraper/temp"


def ensure_temp_dir():
    os.makedirs(TEMP_DIR, exist_ok=True)


def save_temp_results(data: dict) -> str:

    ensure_temp_dir()

    filename = f"live_search_{uuid.uuid4()}.json"
    filepath = os.path.join(TEMP_DIR, filename)

    payload = {
        "created_at": time.time(),
        "data": data
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return filepath