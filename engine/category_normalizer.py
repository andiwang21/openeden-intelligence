def normalize_category(category):

    category = category.lower()

    if "treasury" in category:
        return "Treasury"

    if "stablecoin" in category:
        return "Yield_Bearing_Stablecoin"

    if "staking" in category:
        return "Staking"

    if "lending" in category:
        return "Lending"

    if "credit" in category:
        return "Private_Credit"

    if "structured" in category:
        return "Structured_Product"

    if "gold" in category:
        return "Gold"

    if "quant" in category:
        return "Quant_Strategy"

    return category