import os

from dotenv import load_dotenv

load_dotenv()

print(
    os.getenv(
        "FIRECRAWL_API_KEY"
    )
)

print(
    os.getenv(
        "OPENROUTER_API_KEY"
    )
)