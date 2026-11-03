import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="OpenEden Distribution Intelligence",
    page_icon="🏦",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

PRODUCT_FOLDER = "data/products"

products = []

for file in os.listdir(PRODUCT_FOLDER):

    if file.endswith(".json"):

        try:

            with open(
                os.path.join(PRODUCT_FOLDER, file),
                "r",
                encoding="utf-8"
            ) as f:

                product = json.load(f)

                products.append(product)
                print(
    f"Loaded: {product['exchange']} - {product['product_name']}"
)

        except Exception as e:

            st.error(
                f"Error loading {file}: {e}"
            )

# =====================================================
# SIDEBAR FILTER
# =====================================================

st.sidebar.title("🔎 Filters")

exchange_list = ["All"] + sorted(
    list(
        set(
            p["exchange"]
            for p in products
        )
    )
)

selected_exchange = st.sidebar.selectbox(
    "Exchange",
    exchange_list
)

if selected_exchange != "All":

    products = [
        p for p in products
        if p["exchange"] == selected_exchange
    ]

show_overview = selected_exchange == "All"

# =====================================================
# DATAFRAME
# =====================================================

df = pd.DataFrame(products)

# =====================================================
# HEADER
# =====================================================

st.title("🏦 OpenEden Distribution Intelligence")

st.caption(
    "Mapping Exchanges • Curators • Infrastructure • Yield Sources • OpenEden Distribution Opportunities"
)

# =====================================================
# METRICS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Products",
        len(products)
    )

with col2:

    st.metric(
        "Exchanges",
        len(
            set(
                p["exchange"]
                for p in products
            )
        )
    )

with col3:

    if len(products) > 0:

        avg_yield = round(
            sum(
                p["apy"]
                for p in products
            ) / len(products),
            2
        )

    else:

        avg_yield = 0

    st.metric(
        "Average Yield",
        f"{avg_yield}%"
    )

# =====================================================
# OVERVIEW SECTION
# =====================================================

if show_overview and len(df) > 0:

    st.divider()

    st.subheader("📊 Yield Landscape")

    category_counts = (
        df["category"]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = [
        "Category",
        "Count"
    ]

    fig = px.pie(
        category_counts,
        names="Category",
        values="Count",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("🎯 OpenEden GTM Matrix")

    rows = []

    for p in products:

        rows.append(
            {
                "Exchange": p["exchange"],
                "Product": p["product_name"],
                "Category": p["category"],
                "APY": p["apy"],
                "OpenEden Fit":
                    ", ".join(
                        p["openeden_fit"]
                    )
            }
        )

    matrix_df = pd.DataFrame(rows)

    st.dataframe(
        matrix_df,
        use_container_width=True
    )

# =====================================================
# PRODUCT EXPLORER
# =====================================================

st.divider()

if selected_exchange == "All":

    st.subheader("🏛 Product Explorer")

else:

    st.subheader(f"🏦 {selected_exchange}")


for product in products:

    stack = product["yield_stack"]

    title = product["product_name"]

    if selected_exchange == "All":

        title = (
            f"{product['exchange']} | "
            f"{product['product_name']}"
        )

    with st.expander(

        title,

        expanded=(selected_exchange != "All")

    ):
        

        # -------------------------------------------------
        # TOP METRICS
        # -------------------------------------------------

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
                "OpenEden Fits",
                len(product["openeden_fit"])
            )

        st.divider()

        # -------------------------------------------------
        # ARCHITECTURE
        # -------------------------------------------------

        st.subheader("⚙ Architecture")

        a1, a2, a3 = st.columns(3)

        with a1:

            st.info(
                f"""
Distribution

{stack['distribution']}
"""
            )

        with a2:

            st.info(
                f"""
Curator

{stack['curator']}
"""
            )

        with a3:

            st.info(
                f"""
Infrastructure

{', '.join(stack['infrastructure'])}
"""
            )

        st.divider()

        # -------------------------------------------------
        # COLLATERAL + YIELD SOURCES
        # -------------------------------------------------

        left, right = st.columns(2)

        with left:

            st.subheader("🪙 Collateral")

            for asset in stack["collateral"]:

                st.warning(asset)

        with right:

            st.subheader("💰 Yield Sources")

            for source in stack["yield_source"]:

                st.success(source)

        st.divider()

        # -------------------------------------------------
        # OPENEDEN FIT
        # -------------------------------------------------

        st.subheader("🎯 OpenEden Opportunity")

        for fit in product["openeden_fit"]:

            st.success(fit)

        st.divider()

        # -------------------------------------------------
        # YIELD STACK VISUAL
        # -------------------------------------------------

        st.subheader("🔗 Yield Stack")

        st.markdown(
            f"""
### {stack['distribution']}

⬇️

### {stack['curator']}

⬇️

### {' + '.join(stack['infrastructure'])}

⬇️

### Yield Sources
"""
        )

        for source in stack["yield_source"]:

            st.info(source)

        st.markdown("### Collateral Layer")

        columns = st.columns(
            max(
                1,
                len(stack["collateral"])
            )
        )

        for i, asset in enumerate(
            stack["collateral"]
        ):

            columns[i].warning(asset)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "OpenEden Intelligence Platform v0.2"
)