import pandas as pd
import numpy as np


# ==========================================================
# OVERALL ANALYSIS
# ==========================================================

def load_overall_analysis(df):

    total = df["amount"].sum()
    maximum = df["amount"].max()
    average = df["amount"].mean()
    startups = df["startup"].nunique()

    return total, maximum, average, startups


# ==========================================================
# YEAR ON YEAR
# ==========================================================

def year_on_year(df):

    return (
        df.groupby("year", as_index=False)["amount"]
        .sum()
        .sort_values("year")
    )


# ==========================================================
# MONTH ON MONTH
# ==========================================================

def month_on_month(df):

    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    temp = (
        df.groupby(["year","month"],as_index=False)["amount"]
        .sum()
    )

    temp["month"] = pd.Categorical(
        temp["month"],
        categories=month_order,
        ordered=True
    )

    return temp.sort_values(["year","month"])


# ==========================================================
# TOP STARTUPS
# ==========================================================

def top_startups(df):

    return (
        df.groupby("startup")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )


# ==========================================================
# TOP INVESTORS
# ==========================================================

def top_investors(df):

    temp = df.copy()

    temp["investors"] = (
        temp["investors"]
        .fillna("")
        .str.split(",")
    )

    temp = temp.explode("investors")

    temp["investors"] = temp["investors"].str.strip()

    return (
        temp.groupby("investors")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )


# ==========================================================
# INDUSTRY ANALYSIS
# ==========================================================

def industry_analysis(df):

    return (
        df.groupby("industry")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


# ==========================================================
# FUNDING STAGE
# ==========================================================

def funding_stage_analysis(df):

    return (
        df.groupby("funding_stage")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


# ==========================================================
# CITY ANALYSIS
# ==========================================================

def city_analysis(df):

    return (
        df.groupby("city")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


# ==========================================================
# HEATMAP
# ==========================================================

def funding_heatmap(df):

    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    heatmap = df.pivot_table(
        index="year",
        columns="month",
        values="amount",
        aggfunc="sum"
    )

    heatmap = heatmap.reindex(columns=month_order)

    return heatmap


# ==========================================================
# STARTUP ANALYSIS
# ==========================================================

def startup_details(df, startup):

    return df[df["startup"] == startup].copy()


def startup_history(df, startup):

    return (
        startup_details(df, startup)[
            ["date","funding_stage","amount","investors"]
        ]
        .sort_values("date", ascending=False)
    )


def startup_timeline(df, startup):

    return (
        startup_details(df, startup)
        .sort_values("date")
    )


def startup_investors(df, startup):

    return (
        startup_details(df, startup)[
            ["investors"]
        ]
    )


def similar_companies(df, startup):

    industry = startup_details(df, startup)["industry"].iloc[0]

    return (
        df[
            (df["industry"] == industry) &
            (df["startup"] != startup)
        ][["startup","industry","city"]]
        .drop_duplicates()
    )
# ==========================================================
# INVESTOR ANALYSIS
# ==========================================================

def investor_details(df, investor):

    return df[
        df["investors"].str.contains(
            investor,
            case=False,
            na=False,
            regex=False
        )
    ].copy()


def recent_investments(df, investor):

    return (
        investor_details(df, investor)
        .sort_values("date", ascending=False)
        .head(10)[
            [
                "date",
                "startup",
                "industry",
                "city",
                "funding_stage",
                "amount"
            ]
        ]
    )


def biggest_investments(df, investor):

    return (
        investor_details(df, investor)
        .groupby("startup")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )


def investor_sector(df, investor):

    return (
        investor_details(df, investor)
        .groupby("industry")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


def investor_stage(df, investor):

    return (
        investor_details(df, investor)
        .groupby("funding_stage")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


def investor_city(df, investor):

    return (
        investor_details(df, investor)
        .groupby("city")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


def investor_yoy(df, investor):

    return (
        investor_details(df, investor)
        .groupby("year", as_index=False)["amount"]
        .sum()
        .sort_values("year")
    )


def similar_investors(df, investor):

    startups = investor_details(df, investor)["startup"].unique()

    temp = df[df["startup"].isin(startups)].copy()

    temp["investors"] = (
        temp["investors"]
        .fillna("")
        .str.split(",")
    )

    temp = temp.explode("investors")

    temp["investors"] = temp["investors"].str.strip()

    return (
        temp["investors"]
        .value_counts()
        .drop(investor, errors="ignore")
        .head(10)
    )


# ==========================================================
# DROPDOWN LISTS
# ==========================================================

def startup_list(df):

    return sorted(
        df["startup"]
        .dropna()
        .unique()
    )


def investor_list(df):

    return sorted(

        df["investors"]
        .fillna("")
        .str.split(",")
        .explode()
        .str.strip()
        .replace("", np.nan)
        .dropna()
        .unique()

    )