import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import os
import json

from dotenv import load_dotenv
from firecrawl import FirecrawlApp

from extractors.extract_products import (
    extract_products
)

from extractors.save_products import (
    save_products
)

load_dotenv()

# =====================================
# CONFIG
# =====================================

with open(
    "config/exchanges_to_scan.json",
    "r",
    encoding="utf-8"
) as f:

    exchanges = json.load(f)

os.makedirs(
    "data/raw",
    exist_ok=True
)

firecrawl = FirecrawlApp(
    api_key=os.getenv(
        "FIRECRAWL_API_KEY"
    )
)

# =====================================
# PIPELINE
# =====================================

for exchange in exchanges:

    name = exchange["name"]
    url = exchange["url"]

    print(
        f"\n{'=' * 50}"
    )

    print(
        f"Processing {name}"
    )

    try:

        # ==========================
        # SCRAPE
        # ==========================

        result = firecrawl.scrape_url(
            url,
            formats=["markdown"]
        )

        markdown = result["markdown"]

        raw_file = (
            f"data/raw/{name}.md"
        )

        with open(
            raw_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(markdown)

        print(
            f"Saved {raw_file}"
        )

        # ==========================
        # EXTRACT
        # ==========================

        products = extract_products(
            markdown
        )

        print(
            f"Found {len(products)} products"
        )

        # ==========================
        # SAVE
        # ==========================

        save_products(products)

        print(
            f"Completed {name}"
        )

    except Exception as e:

        print(
            f"FAILED {name}"
        )

        print(e)