import os

from dotenv import load_dotenv
from firecrawl import FirecrawlApp

load_dotenv()

app = FirecrawlApp(
    api_key=os.getenv(
        "FIRECRAWL_API_KEY"
    )
)

url = "https://www.coinbase.com/earn"

result = app.scrape_url(
    url,
    formats=["markdown"]
)

markdown_content = result["markdown"]

print(
    markdown_content[:5000]
)

with open(
    "coinbase_earn.md",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        markdown_content
    )

print(
    "✅ Saved coinbase_earn.md"
)