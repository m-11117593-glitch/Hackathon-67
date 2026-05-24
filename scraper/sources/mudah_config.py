from dataclasses import dataclass


@dataclass
class MudahCategory:
    name: str
    weight: int
    url_builder: callable
    max_pages: int
    use_query_param: bool  # whether uses ?q= style pagination


# -----------------------------
# APARTMENT / CONDO
# -----------------------------
def build_apartment(state: str, page: int = 1) -> str:
    return f"https://www.mudah.my/{state}/apartment-condominium-for-sale?o={page}"


# -----------------------------
# 2 STORY HOUSE
# -----------------------------
def build_house_2story(state: str, page: int = 1) -> str:
    return f"https://www.mudah.my/malaysia/houses-for-sale?o={page}&q={state}+2+story+house"


# -----------------------------
# 1 STORY HOUSE
# -----------------------------
def build_house_1story(state: str, page: int = 1) -> str:
    return f"https://www.mudah.my/malaysia/houses-for-sale?o={page}&q={state}+1+story+house"


# -----------------------------
# BUNGALOW
# -----------------------------
def build_bungalow(state: str, page: int = 1) -> str:
    return f"https://www.mudah.my/malaysia/houses-for-sale?o={page}&q={state}+bungalow+house"


# -----------------------------
# OTHER
# -----------------------------
def build_other(state: str, page: int = 1) -> str:
    return f"https://www.mudah.my/malaysia/properties-for-sale?o={page}&q={state}"


MUDAH_CATEGORIES = [
    MudahCategory("condominium", 30, build_apartment, max_pages=5, use_query_param=False),
    MudahCategory("2story", 25, build_house_2story, max_pages=2, use_query_param=True),
    MudahCategory("1story", 15, build_house_1story, max_pages=2, use_query_param=True),
    MudahCategory("bungalow", 10, build_bungalow, max_pages=3, use_query_param=True),
    MudahCategory("other", 10, build_other, max_pages=8, use_query_param=True),
]