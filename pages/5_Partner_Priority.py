import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(
    page_title="Partner Priority",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 OpenEden Partner Priority Engine")

# ======================================
# LOAD PRODUCTS
# ======================================

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

# ======================================
# COMPLETE PRODUCT SHELF
# ======================================

all_categories = [

    "Treasury",
    "Yield_Bearing_Stablecoin",
    "Private_Credit",
    "Structured_Product",
    "Gold",
    "Quant_Strategy"

]

category_to_product = {

    "Treasury": "TBILL",
    "Yield_Bearing_Stablecoin": "cUSDO",
    "Private_Credit": "HYBOND",
    "Structured_Product": "FCN",
    "Gold": "GOLD+",
    "Quant_Strategy": "QIS"
}

# ======================================
# CALCULATE SCORES
# ======================================

results = []

exchanges = sorted(
    list(
        set(
            p["exchange"]
            for p in products
        )
    )
)

for exchange in exchanges:

    exchange_products = [

        p for p in products

        if p["exchange"] == exchange
    ]

    categories = list(
        set(
            p["category"]
            for p in exchange_products
        )
    )

    missing = [

        c for c in all_categories

        if c not in categories
    ]

    recommendations = [

        category_to_product[c]

        for c in missing

        if c in category_to_product
    ]

    score = len(missing) * 15

    if "Structured_Product" in missing:
        score += 20

    if "Treasury" in missing:
        score += 15

    if "Yield_Bearing_Stablecoin" in missing:
        score += 15

    results.append(
        {
            "Exchange": exchange,
            "Priority Score": score,
            "Categories Covered":
                len(categories),

            "Missing":
                ", ".join(missing),

            "Recommended Products":
                ", ".join(recommendations)
        }
    )

# ======================================
# SORT
# ======================================

results = sorted(
    results,
    key=lambda x: x["Priority Score"],
    reverse=True
)

df = pd.DataFrame(results)

# ======================================
# LEADERBOARD
# ======================================

st.subheader("🏆 Priority Ranking")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ======================================
# TOP TARGETS
# ======================================

st.divider()

st.subheader("🎯 Top Targets This Week")

top_targets = results[:3]

for target in top_targets:

    st.success(
        f"""
{target['Exchange']}

Priority Score:
{target['Priority Score']}

Recommended:
{target['Recommended Products']}
"""
    )

# ======================================
# GTM PLAYBOOK
# ======================================

st.divider()

st.subheader("🚀 GTM Playbook")

selected_exchange = st.selectbox(
    "Select Exchange",
    df["Exchange"]
)

target = next(
    x for x in results
    if x["Exchange"] == selected_exchange
)

st.info(
    f"""
Exchange:
{target['Exchange']}

Priority:
{target['Priority Score']}

Missing Categories:
{target['Missing']}

Recommended OpenEden Products:
{target['Recommended Products']}
"""
)
