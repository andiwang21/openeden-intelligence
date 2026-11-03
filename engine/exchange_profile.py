def build_exchange_profile(
    exchange,
    products
):

    exchange_products = [

        p for p in products

        if p["exchange"]
        == exchange
    ]

    categories = sorted(

        list(
            set(
                p["category"]
                for p in exchange_products
            )
        )
    )

    partnerships = []

    for product in exchange_products:

        partnerships.extend(
            product.get(
                "partnerships",
                []
            )
        )

    partnerships = sorted(
        list(
            set(
                partnerships
            )
        )
    )

    return {

        "exchange":
            exchange,

        "product_count":
            len(
                exchange_products
            ),

        "categories":
            categories,

        "partnerships":
            partnerships
    }