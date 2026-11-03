import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(
    page_title="OpenEden GTM Engine",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 OpenEden GTM Engine")

# ====================================
# LOAD PRODUCTS
# ====================================

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

# ====================================
# MARKET TAXONOMY
# ====================================

all_categories = [
    "Treasury",
    "Yield_Bearing_Stablecoin",
    "Private_Credit",
    "Structured_Product",
    "Gold",
    "Quant_Strategy"
]

product_mapping = {
    "Treasury": "TBILL",
    "Yield_Bearing_Stablecoin": "cUSDO",
    "Private_Credit": "HYBOND",
    "Structured_Product": "FCN",
    "Gold": "GOLD+",
    "Quant_Strategy": "QIS"
}

# ====================================
# EXCHANGES
# ====================================

exchanges = sorted(
    list(
        set(
            p["exchange"]
            for p in products
        )
    )
)

selected_exchange = st.selectbox(
    "Exchange",
    exchanges
)

exchange_products = [

    p for p in products

    if p["exchange"]
    == selected_exchange
]

# ====================================
# CURRENT COVERAGE
# ====================================

current_categories = list(
    set(
        p["category"]
        for p in exchange_products
    )
)

missing_categories = [

    c
    for c in all_categories

    if c not in current_categories
]

recommended_products = [

    product_mapping[c]

    for c in missing_categories

    if c in product_mapping
]

# ====================================
# SCORE
# ====================================

coverage_score = int(

    (
        len(current_categories)
        /
        len(all_categories)
    ) * 100
)

# ====================================
# DASHBOARD
# ====================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Coverage Score",
        f"{coverage_score}/100"
    )

with c2:

    st.metric(
        "Categories Covered",
        len(current_categories)
    )

with c3:

    st.metric(
        "Missing Categories",
        len(missing_categories)
    )

st.divider()

# ====================================
# CURRENT SHELF
# ====================================

left, right = st.columns(2)

with left:

    st.subheader("✅ Current Shelf")

    for category in current_categories:

        st.success(category)

with right:

    st.subheader("❌ Missing Categories")

    for category in missing_categories:

        st.warning(category)

st.divider()

# ====================================
# OPENEDEN PITCH
# ====================================

st.subheader("🚀 OpenEden Products To Pitch")

if len(recommended_products) > 0:

    for product in recommended_products:

        st.success(product)

else:

    st.success(
        "Full category coverage"
    )

st.divider()

# ====================================
# STRATEGIC TALK TRACK
# ====================================

st.subheader("🧠 GTM Recommendation")

if len(recommended_products) > 0:

    st.info(
        f"""
{selected_exchange} currently lacks:

{", ".join(missing_categories)}

Recommended discussion:

{", ".join(recommended_products)}

Priority should focus on adding
new yield categories rather than
duplicating existing products.
"""
    )

else:

    st.info(
        f"""
{selected_exchange}
already covers all tracked categories.

Focus should shift toward:

• Collateral utility
• Better yield packaging
• Distribution expansion
"""
    )