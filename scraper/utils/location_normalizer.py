import re


STATE_MAPPINGS = {
    "kuala lumpur": "kuala-lumpur",
    "pulau pinang": "penang",
    "penang": "penang",
    "negeri sembilan": "negeri-sembilan",
}


def slugify(text: str) -> str:
    text = text.lower().strip()

    text = re.sub(r"[,\s]+", "-", text)

    text = re.sub(r"-+", "-", text)

    return text.strip("-")


def normalize_location(location: str) -> str:

    if not location:
        return "malaysia"

    location = location.lower().strip()

    for key, value in STATE_MAPPINGS.items():
        location = location.replace(key, value)

    location = slugify(location)

    return location