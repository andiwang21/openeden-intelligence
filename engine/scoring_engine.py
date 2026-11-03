def calculate_tbill_score(product):

    score = 0

    institutional = product.get(
        "institutional_features",
        {}
    )

    if institutional.get(
        "rwa_support",
        False
    ):
        score += 40

    if institutional.get(
        "prime_broker_ready",
        False
    ):
        score += 20

    if institutional.get(
        "off_exchange_collateral",
        False
    ):
        score += 20

    if (
        product["category"]
        ==
        "Yield_Bearing_Stablecoin"
    ):
        score += 20

    return min(score, 100)


def calculate_cusdo_score(product):

    score = 0

    institutional = product.get(
        "institutional_features",
        {}
    )

    if institutional.get(
        "off_exchange_collateral",
        False
    ):
        score += 50

    if institutional.get(
        "prime_broker_ready",
        False
    ):
        score += 30

    score += 20

    return min(score, 100)


def calculate_hybond_score(product):

    score = 0

    if (
        product["category"]
        ==
        "Private_Credit"
    ):
        score += 50

    score += 30

    return min(score, 100)


def calculate_fcn_score(product):

    score = 0

    signals = product.get(
        "competitive_signals",
        {}
    )

    if signals.get(
        "structured_products",
        False
    ):
        score += 70

    score += 20

    return min(score, 100)


def score_product(product):

    return {

        "tbill":
            calculate_tbill_score(
                product
            ),

        "cusdo":
            calculate_cusdo_score(
                product
            ),

        "hybond":
            calculate_hybond_score(
                product
            ),

        "fcn":
            calculate_fcn_score(
                product
            )
    }