from copy import deepcopy


def generate_query_variants(filters: dict):

    variants = []

    base = deepcopy(filters)

    variants.append(base)

    if base.get("car_park"):
        v2 = deepcopy(base)
        v2["car_park"] = False
        variants.append(v2)

    if base.get("bedrooms"):
        v3 = deepcopy(base)
        v3["bedrooms"] = None
        variants.append(v3)

    v4 = deepcopy(base)
    v4["bedrooms"] = None
    v4["car_park"] = False
    v4["budget"] = int(base.get("budget", 0) * 1.2)

    variants.append(v4)

    return variants