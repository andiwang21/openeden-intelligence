import streamlit as st
import json
import os

st.set_page_config(
    page_title="Ecosystem Comparison",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Ecosystem Comparison")

# =====================================================
# LOAD PRODUCTS
# =====================================================

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

# =====================================================
# SELECT PRODUCTS
# =====================================================

product_names = [
    p["product_name"]
    for p in products
]

selected_products = st.multiselect(
    "Products",
    product_names,
    default=product_names
)

products = [
    p for p in products
    if p["product_name"] in selected_products
]

if len(products) == 0:

    st.warning("Select at least one product")

    st.stop()

# =====================================================
# PRODUCT HEADER ROW
# =====================================================

st.subheader("Products")

cols = st.columns(len(products))

for i, p in enumerate(products):

    cols[i].markdown(
        f"""
### {p["exchange"]}

{p["product_name"]}

**{p["apy"]}% APY**
"""
    )

# =====================================================
# HELPER
# =====================================================

def render_row(title, icon, color, extractor):

    st.divider()

    st.markdown(
        f"## {icon} {title}"
    )

    cols = st.columns(len(products))

    for idx, p in enumerate(products):

        data = extractor(p)

        if isinstance(data, list):

            text = "<br>".join(data)

        else:

            text = str(data)

        cols[idx].markdown(
            f"""
<div style="
padding:14px;
border-radius:12px;
background:{color};
min-height:120px;
">
{text}
</div>
""",
            unsafe_allow_html=True
        )

# =====================================================
# ROWS
# =====================================================

render_row(
    "Category",
    "📦",
    "#24344d",
    lambda p: p["category"]
)

render_row(
    "Distribution",
    "🏦",
    "#1f3d2b",
    lambda p: p["yield_stack"]["distribution"]
)

render_row(
    "Curator",
    "🧠",
    "#4d3b1f",
    lambda p: p["yield_stack"]["curator"]
)

render_row(
    "Infrastructure",
    "⚙️",
    "#163c33",
    lambda p: p["yield_stack"]["infrastructure"]
)

render_row(
    "Collateral",
    "🪙",
    "#24344d",
    lambda p: p["yield_stack"]["collateral"]
)

render_row(
    "Yield Sources",
    "💰",
    "#4a2525",
    lambda p: p["yield_stack"]["yield_source"]
)

render_row(
    "OpenEden Fit",
    "🎯",
    "#224422",
    lambda p: p["openeden_fit"]
)