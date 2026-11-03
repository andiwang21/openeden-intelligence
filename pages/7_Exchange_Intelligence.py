import streamlit as st
import json
import os

from engine.exchange_profile import (
    build_exchange_profile
)

st.set_page_config(
    page_title="Exchange Intelligence",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Exchange Intelligence")

# ==========================================
# LOAD PRODUCTS
# ==========================================

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

# ==========================================
# EXCHANGE SELECTOR
# ==========================================

exchange_names = sorted(
    list(
        set(
            p["exchange"]
            for p in products
        )
    )
)

selected_exchange = st.selectbox(
    "Exchange",
    exchange_names
)

profile = build_exchange_profile(
    selected_exchange,
    products
)

exchange_products = [

    p for p in products

    if p["exchange"]
    == selected_exchange
]

# ==========================================
# TOP METRICS
# ==========================================

m1, m2, m3 = st.columns(3)

with m1:

    st.metric(
        "Products",
        profile["product_count"]
    )

with m2:

    st.metric(
        "Categories",
        len(
            profile["categories"]
        )
    )

with m3:

    st.metric(
        "Partnerships",
        len(
            profile["partnerships"]
        )
    )

st.divider()

# ==========================================
# CATEGORIES + PARTNERS
# ==========================================

left, right = st.columns(2)

with left:

    st.subheader(
        "📚 Product Categories"
    )

    for category in profile["categories"]:

        st.success(category)

with right:

    st.subheader(
        "🤝 Partnerships"
    )

    if len(profile["partnerships"]) == 0:

        st.info(
            "No partnerships mapped"
        )

    else:

        for partner in profile["partnerships"]:

            st.info(partner)

st.divider()

# ==========================================
# PRODUCT SHELF
# ==========================================

st.subheader(
    "📦 Product Shelf"
)

categories = {}

for product in exchange_products:

    category = product["category"]

    if category not in categories:

        categories[category] = []

    categories[category].append(product)

for category, products_in_category in categories.items():

    st.markdown(
        f"## {category}"
    )

    for product in products_in_category:

        stack = product["yield_stack"]

        with st.expander(
            product["product_name"],
            expanded=False
        ):

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Category",
                    product["category"]
                )

            with c2:

                st.metric(
                    "APY",
                    f"{product['apy']}%"
                )

            with c3:

                st.metric(
                    "Priority",
                    product.get(
                        "gtm",
                        {}
                    ).get(
                        "priority_score",
                        0
                    )
                )

            st.divider()

            left, right = st.columns(2)

            with left:

                st.subheader(
                    "Infrastructure"
                )

                for infra in stack.get(
                    "infrastructure",
                    []
                ):

                    st.success(infra)

                st.subheader(
                    "Collateral"
                )

                for collateral in stack.get(
                    "collateral",
                    []
                ):

                    st.warning(collateral)

            with right:

                st.subheader(
                    "Yield Sources"
                )

                for source in stack.get(
                    "yield_source",
                    []
                ):

                    st.info(source)

                st.subheader(
                    "Partnerships"
                )

                for partner in product.get(
                    "partnerships",
                    []
                ):

                    st.success(partner)

    st.divider()

# ==========================================
# OPENEDEN OPPORTUNITIES
# ==========================================

st.subheader(
    "🎯 OpenEden Opportunities"
)

all_fits = []

for product in exchange_products:

    all_fits.extend(
        product.get(
            "openeden_fit",
            []
        )
    )

all_fits = sorted(
    list(
        set(all_fits)
    )
)

if len(all_fits) == 0:

    st.info(
        "No OpenEden opportunities mapped yet."
    )

else:

    fit_cols = st.columns(
        len(all_fits)
    )

    for idx, fit in enumerate(
        all_fits
    ):

        fit_cols[idx].success(
            fit
        )

st.divider()

# ==========================================
# GTM INTELLIGENCE
# ==========================================

st.subheader(
    "🧠 GTM Intelligence"
)

summary = f"""
{selected_exchange} currently offers
{profile['product_count']} tracked products across
{len(profile['categories'])} product categories.

Product Categories:
{", ".join(profile['categories'])}

Partnerships:
{", ".join(profile['partnerships']) if profile['partnerships'] else "Not mapped"}

OpenEden Opportunities:
{", ".join(all_fits) if all_fits else "Not mapped"}
"""

st.info(summary)