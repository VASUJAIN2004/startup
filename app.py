import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import helper

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="Startup Funding Explorer",
    layout="wide"
)

# ======================================
# LOAD DATA
# ======================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/cleaned_startup_funding.csv")
    df["date"] = pd.to_datetime(df["date"])

    return df


df = load_data()

# ======================================
# SIDEBAR
# ======================================

st.sidebar.title("Startup Funding Explorer")

option = st.sidebar.selectbox(
    "Select Analysis",
    (
        "Overall Analysis",
        "Startup Analysis",
        "Investor Analysis"
    )
)

# ======================================
# OVERALL ANALYSIS
# ======================================

if option == "Overall Analysis":

    st.title("Overall Startup Funding Analysis")

    total, maximum, average, startups = helper.load_overall_analysis(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Funding", f"${total:,.0f}")
    c2.metric("Highest Funding", f"${maximum:,.0f}")
    c3.metric("Average Funding", f"${average:,.0f}")
    c4.metric("Funded Startups", startups)

    st.divider()

    # ---------------------------
    # YEAR ON YEAR
    # ---------------------------

    st.subheader("Year on Year Funding")

    yoy = helper.year_on_year(df)

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(
        yoy["year"],
        yoy["amount"],
        marker="o",
        linewidth=3
    )

    ax.grid(True)

    st.pyplot(fig)

    st.divider()

    # ---------------------------
    # MONTH ON MONTH
    # ---------------------------

    st.subheader("Month on Month Funding")

    mom = helper.month_on_month(df)

    fig, ax = plt.subplots(figsize=(12,4))

    ax.plot(
        range(len(mom)),
        mom["amount"],
        marker="o"
    )

    ax.set_xticks(range(len(mom)))

    ax.set_xticklabels(
        mom["month"].astype(str),
        rotation=90
    )

    ax.grid(True)

    st.pyplot(fig)

    st.divider()
    # =====================================
    # TOP STARTUPS
    # =====================================

    st.subheader("Top 10 Funded Startups")

    startups = helper.top_startups(df)

    col1, col2 = st.columns([1,2])

    with col1:
        st.dataframe(startups)

    with col2:

        fig, ax = plt.subplots(figsize=(8,4))

        ax.bar(startups.index, startups.values)

        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()

        st.pyplot(fig)

    st.divider()

    # =====================================
    # TOP INVESTORS
    # =====================================

    st.subheader("Top 10 Investors")

    investors = helper.top_investors(df)

    col1, col2 = st.columns([1,2])

    with col1:
        st.dataframe(investors)

    with col2:

        fig, ax = plt.subplots(figsize=(8,4))

        ax.bar(investors.index, investors.values)

        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()

        st.pyplot(fig)

    st.divider()

    # =====================================
    # INDUSTRY WISE FUNDING
    # =====================================

    st.subheader("Industry Wise Funding")

    industry = helper.industry_analysis(df).head(10)

    fig, ax = plt.subplots(figsize=(7,7))

    ax.pie(
        industry,
        labels=industry.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)

    st.divider()

    # =====================================
    # FUNDING STAGE
    # =====================================

    st.subheader("Funding Stage")

    stage = helper.funding_stage_analysis(df)

    fig, ax = plt.subplots(figsize=(7,7))

    ax.pie(
        stage,
        labels=stage.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)

    st.divider()

    # =====================================
    # CITY WISE FUNDING
    # =====================================

    st.subheader("Top Cities")

    city = helper.city_analysis(df).head(10)

    fig, ax = plt.subplots(figsize=(10,4))

    ax.bar(city.index, city.values)

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    st.pyplot(fig)

    st.divider()

    # =====================================
    # HEATMAP
    # =====================================

    st.subheader("Funding Heatmap")

    heatmap = helper.funding_heatmap(df).fillna(0)

    fig, ax = plt.subplots(figsize=(12,5))

    img = ax.imshow(
        heatmap,
        aspect="auto"
    )

    ax.set_xticks(range(len(heatmap.columns)))
    ax.set_xticklabels(
        heatmap.columns,
        rotation=45
    )

    ax.set_yticks(range(len(heatmap.index)))
    ax.set_yticklabels(heatmap.index)

    plt.colorbar(img)

    st.pyplot(fig)
# ======================================
# STARTUP ANALYSIS
# ======================================

elif option == "Startup Analysis":

    st.title("Startup Analysis")

    startup = st.sidebar.selectbox(
        "Select Startup",
        helper.startup_list(df)
    )

    startup_df = helper.startup_details(df, startup)

    latest = startup_df.iloc[-1]

    # ======================================
    # COMPANY DETAILS
    # ======================================

    st.header(startup)

    c1, c2, c3 = st.columns(3)

    c1.metric("Industry", latest["industry"])
    c2.metric("Sub Industry", latest["subindustry"])
    c3.metric("City", latest["city"])

    c1, c2, c3 = st.columns(3)

    c1.metric("Funding Stage", latest["funding_stage"])
    c2.metric("Funding Rounds", len(startup_df))
    c3.metric(
        "Total Funding",
        f"${startup_df['amount'].sum():,.0f}"
    )

    st.divider()

    # ======================================
    # FUNDING HISTORY
    # ======================================

    st.subheader("Funding History")

    st.dataframe(
        helper.startup_history(df, startup),
        use_container_width=True
    )

    st.divider()

    # ======================================
    # FUNDING TIMELINE
    # ======================================

    st.subheader("Funding Timeline")

    timeline = helper.startup_timeline(df, startup)

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(
        timeline["date"],
        timeline["amount"],
        marker="o",
        linewidth=3
    )

    ax.grid(True)

    st.pyplot(fig)

    st.divider()

    # ======================================
    # INVESTORS
    # ======================================

    st.subheader("Investors")

    st.dataframe(
        helper.startup_investors(df, startup),
        use_container_width=True
    )

    st.divider()

    # ======================================
    # SIMILAR COMPANIES
    # ======================================

    st.subheader("Similar Companies")

    st.dataframe(
        helper.similar_companies(df, startup),
        use_container_width=True
    )
# ======================================
# INVESTOR ANALYSIS
# ======================================

elif option == "Investor Analysis":

    st.title("Investor Analysis")

    investor = st.sidebar.selectbox(
        "Select Investor",
        helper.investor_list(df)
    )

    st.header(investor)

    # ======================================
    # RECENT INVESTMENTS
    # ======================================

    st.subheader("Recent Investments")

    st.dataframe(
        helper.recent_investments(df, investor),
        use_container_width=True
    )

    st.divider()

    # ======================================
    # BIGGEST INVESTMENTS
    # ======================================

    st.subheader("Biggest Investments")

    biggest = helper.biggest_investments(df, investor)

    col1, col2 = st.columns([1,2])

    with col1:
        st.dataframe(biggest)

    with col2:

        fig, ax = plt.subplots(figsize=(8,4))

        ax.bar(
            biggest.index,
            biggest.values
        )

        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()

        st.pyplot(fig)

    st.divider()

    # ======================================
    # PIE CHARTS
    # ======================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Industry Wise Investments")

        sector = helper.investor_sector(df, investor)

        fig, ax = plt.subplots(figsize=(6,6))

        ax.pie(
            sector,
            labels=sector.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.axis("equal")

        st.pyplot(fig)

    with col2:

        st.subheader("Funding Stage")

        stage = helper.investor_stage(df, investor)

        fig, ax = plt.subplots(figsize=(6,6))

        ax.pie(
            stage,
            labels=stage.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.axis("equal")

        st.pyplot(fig)

    st.divider()

    # ======================================
    # CITY ANALYSIS
    # ======================================

    st.subheader("City Wise Investments")

    city = helper.investor_city(df, investor)

    fig, ax = plt.subplots(figsize=(7,7))

    ax.pie(
        city,
        labels=city.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)

    st.divider()

    # ======================================
    # YEAR ON YEAR
    # ======================================

    st.subheader("Year on Year Investments")

    yoy = helper.investor_yoy(df, investor)

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(
        yoy["year"],
        yoy["amount"],
        marker="o",
        linewidth=3
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Funding Amount")
    ax.grid(True)

    st.pyplot(fig)

    st.divider()

    # ======================================
    # SIMILAR INVESTORS
    # ======================================

    st.subheader("Similar Investors")

    similar = helper.similar_investors(df, investor)

    col1, col2 = st.columns([1,2])

    with col1:
        st.dataframe(similar)

    with col2:

        fig, ax = plt.subplots(figsize=(8,4))

        ax.bar(
            similar.index,
            similar.values
        )

        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()

        st.pyplot(fig)