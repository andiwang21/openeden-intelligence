import os

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

COINBASE_URL = "https://www.coinbase.com/earn"

RAW_FILE = "data/raw/coinbase.md"

os.makedirs(
    "data/raw",
    exist_ok=True
)

# =====================================
# FIRECRAWL
# =====================================

firecrawl = FirecrawlApp(
    api_key=os.getenv(
        "FIRECRAWL_API_KEY"
    )
)

# =====================================
# STEP 1
# SCRAPE
# =====================================

print(
    "Scraping Coinbase..."
)

result = firecrawl.scrape_url(
    COINBASE_URL,
    formats=["markdown"]
)

markdown = result["markdown"]

with open(
    RAW_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(markdown)

print(
    "Saved raw markdown"
)

# =====================================
# STEP 2
# EXTRACT
# =====================================

print(
    "Extracting products..."
)

products = extract_products(
    markdown
)

print(
    f"Found {len(products)} products"
)

# =====================================
# STEP 3
# SAVE
# =====================================

save_products(products)

print(
    "Pipeline completed"
)