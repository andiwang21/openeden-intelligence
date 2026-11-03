import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    ),
    base_url="https://openrouter.ai/api/v1"
)

def extract_products(markdown):

    prompt = f"""
You are an OpenEden intelligence analyst.

Extract every yield-bearing product.

Category MUST be one of:

Treasury
Yield_Bearing_Stablecoin
Private_Credit
Structured_Product
Gold
Quant_Strategy
Lending
Staking

Return ONLY raw JSON.

Do not use markdown.
Do not use code fences.

Format:

[
  {{
    "exchange": "",
    "product_name": "",
    "category": "",
    "apy": 0,
    "infrastructure": "",
    "partnerships": [],
    "collateral": [],
    "yield_source": []
  }}
]

Markdown:

{markdown[:20000]}
"""

    response = client.chat.completions.create(

        model="deepseek/deepseek-chat",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    content = content.strip()

    return json.loads(content)