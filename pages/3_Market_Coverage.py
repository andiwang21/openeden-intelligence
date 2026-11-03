import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(
    page_title="Market Coverage",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Market Coverage")

products = []

for file in os.listdir("data/products"):

    if file.endswith(".json"):

        with open(
            os.path.join(
                "data/products",
                file
            ),
            "r",
            encoding="utf-8"
        ) as f:

            products.append(
                json.load(f)
            )

exchanges = sorted(
    list(
        set(
            p["exchange"]
            for p in products
        )
    )
)

categories = sorted(
    list(
        set(
            p["category"]
            for p in products
        )
    )
)

coverage = []

for category in categories:

    row = {
        "Category": category
    }

    for exchange in exchanges:

        found = any(

            p["exchange"] == exchange
            and
            p["category"] == category

            for p in products
        )

        row[exchange] = "✅" if found else "❌"

    coverage.append(row)

df = pd.DataFrame(coverage)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)