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

with open(
    "coinbase_earn.md",
    "r",
    encoding="utf-8"
) as f:

    markdown = f.read()

prompt = f"""
You are an OpenEden intelligence analyst.

Extract EVERY yield product offered.

For each product return:

- exchange
- product_name
- category
- apy
- infrastructure
- partnerships
- collateral
- yield_source

Output ONLY valid JSON.

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

print(
    response.choices[0].message.content
)