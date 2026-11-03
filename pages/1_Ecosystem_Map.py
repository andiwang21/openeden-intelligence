import streamlit as st
import json
import os

st.set_page_config(
    page_title="Ecosystem Map",
    layout="wide"
)

st.title("🕸 OpenEden Yield Ecosystem")

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

selected = st.selectbox(
    "Product",
    [p["product_name"] for p in products]
)

product = next(
    p for p in products
    if p["product_name"] == selected
)

stack = product["yield_stack"]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.subheader("Distribution")

    st.info(
        stack["distribution"]
    )

with col2:

    st.subheader("Curator")

    st.info(
        stack["curator"]
    )

with col3:

    st.subheader("Infrastructure")

    for infra in stack["infrastructure"]:

        st.warning(infra)

with col4:

    st.subheader("Collateral")

    for asset in stack["collateral"]:

        st.success(asset)

with col5:

    st.subheader("Yield Source")

    for source in stack["yield_source"]:

        st.error(source)

st.divider()

st.subheader("OpenEden Opportunity")

for fit in product["openeden_fit"]:

    st.success(fit)
