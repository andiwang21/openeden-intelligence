from engine.category_normalizer import (
    normalize_category
)

import json
import os
import re

PRODUCT_FOLDER = "data/products"

os.makedirs(
    PRODUCT_FOLDER,
    exist_ok=True
)

def save_products(products):

    for product in products:

        filename = (
            f"{product['exchange']}_"
            f"{product['product_name']}"
            .lower()
        )

        filename = re.sub(
            r'[^a-z0-9_]',
            "_",
            filename
        )

        filepath = os.path.join(
            PRODUCT_FOLDER,
            f"{filename}.json"
        )

        payload = {

            "exchange":
                product["exchange"],

            "exchange_tier":
                1,

            "product_name":
                product["product_name"],

            "product_status":
                "live",

            "category":
                normalize_category(
                        product["category"]
                ),

            "subcategory":
                "",

            "apy":
                product["apy"],

            "tvl":
                None,

            "aum":
                None,

            "yield_stack": {

                "distribution":
                    product["exchange"],

                "curator":
                    "",

                "allocator":
                    "",

                "infrastructure":
                    [product["infrastructure"]],

                "custody":
                    [],

                "collateral":
                    product["collateral"],

                "yield_source":
                    product["yield_source"],

                "reward_layer":
                    []
            },

            "partnerships":
                product["partnerships"],

            "campaigns":
                [],

            "integrations":
                [],

            "openeden_fit": [],

            "data_source":
                "pipeline",

            "last_updated":
                "2026-11-02"
        }

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                payload,
                f,
                indent=4
            )

        print(
            f"Saved {filepath}"
        )