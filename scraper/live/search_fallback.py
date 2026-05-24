from copy import deepcopy


def generate_query_variants(filters: dict):

    """
    Creates fallback search stages:

    1. strict (all filters)
    2. no car park
    3. no bedrooms
    4. broad search
    """

    variants = []

    base = deepcopy(filters)

    # ---------------- STAGE 1: STRICT ----------------
    variants.append(base)

    # ---------------- STAGE 2: REMOVE CAR PARK ----------------
    if base.get("car_park"):

        v2 = deepcopy(base)
        v2["car_park"] = False
        variants.append(v2)

    # ---------------- STAGE 3: REMOVE BEDROOMS ----------------
    if base.get("bedrooms"):

        v3 = deepcopy(base)
        v3["bedrooms"] = None
        variants.append(v3)

    # ---------------- STAGE 4: BROAD SEARCH ----------------
    v4 = deepcopy(base)
    v4["bedrooms"] = None
    v4["car_park"] = False
    v4["budget"] = int(base.get("budget", 0) * 1.2)  # slightly broader
    variants.append(v4)

    return variants