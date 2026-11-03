import streamlit as st
import json
import os

from engine.scoring_engine import (
    score_product
)

st.title(
    "🧪 OpenEden Scoring Lab"
)

products = []

for file in os.listdir(
    "data/products"
):

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

for product in products:

    scores = score_product(
        product
    )

    st.subheader(
        product["exchange"]
    )

    st.json(scores)