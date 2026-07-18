#preprocessing.py
#
# This will:
#
# Read the Kaggle dataset
# Clean missing values
# Convert dates
# Clean funding amounts
# Standardize city names
# Rename columns
# Create new features (year, month, quarter)
# Save a cleaned datase
import pandas as pd
import numpy as np


class DataPreprocessor:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    # ---------------------------------------------------------
    # Load Dataset
    # ---------------------------------------------------------

    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print("Dataset Loaded Successfully")
        print(f"Shape : {self.df.shape}")

    # ---------------------------------------------------------
    # Rename Columns
    # ---------------------------------------------------------

    def rename_columns(self):

        self.df.rename(columns={
            "Sr No": "sr_no",
            "Date dd/mm/yyyy": "date",
            "Startup Name": "startup",
            "Industry Vertical": "industry",
            "SubVertical": "subindustry",
            "City  Location": "city",
            "City Location": "city",
            "Investors Name": "investors",
            "InvestmentnType": "funding_stage",
            "Amount in USD": "amount",
            "Remarks": "remarks"
        }, inplace=True)

    # ---------------------------------------------------------
    # Remove Duplicate Rows
    # ---------------------------------------------------------

    def remove_duplicates(self):

        before = len(self.df)

        self.df.drop_duplicates(inplace=True)

        after = len(self.df)

        print(f"Duplicates Removed : {before-after}")

    # ---------------------------------------------------------
    # Clean Date
    # ---------------------------------------------------------

    def clean_dates(self):

        self.df["date"] = pd.to_datetime(
            self.df["date"],
            dayfirst=True,
            errors="coerce"
        )

        self.df["year"] = self.df["date"].dt.year
        self.df["month"] = self.df["date"].dt.month_name()
        self.df["quarter"] = self.df["date"].dt.quarter

    # ---------------------------------------------------------
    # Clean Text Columns
    # ---------------------------------------------------------

    def clean_text(self):

        text_columns = [
            "startup",
            "industry",
            "subindustry",
            "city",
            "investors",
            "funding_stage"
        ]

        for col in text_columns:

            self.df[col] = (
                self.df[col]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
            )

    # ---------------------------------------------------------
    # Standardize City Names
    # ---------------------------------------------------------

    def standardize_city(self):

        city_mapping = {

            "Bangalore": "Bengaluru",
            "Bengaluru": "Bengaluru",

            "Delhi": "Delhi NCR",
            "New Delhi": "Delhi NCR",
            "Delhi/NCR": "Delhi NCR",
            "Noida": "Delhi NCR",
            "Gurgaon": "Delhi NCR",
            "Gurugram": "Delhi NCR",

            "Bombay": "Mumbai",

            "N/A": "Unknown",
            "nan": "Unknown"
        }

        self.df["city"] = self.df["city"].replace(city_mapping)

    # ---------------------------------------------------------
    # Clean Funding Amount
    # ---------------------------------------------------------

    def clean_amount(self):

        self.df["amount"] = (
            self.df["amount"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.strip()
        )

        self.df["amount"] = pd.to_numeric(
            self.df["amount"],
            errors="coerce"
        )

    # ---------------------------------------------------------
    # Fill Missing Values
    # ---------------------------------------------------------

    def fill_missing(self):

        self.df["industry"] = self.df["industry"].fillna("Unknown")
        self.df["subindustry"] = self.df["subindustry"].fillna("Unknown")
        self.df["city"] = self.df["city"].fillna("Unknown")
        self.df["investors"] = self.df["investors"].fillna("Undisclosed")
        self.df["funding_stage"] = self.df["funding_stage"].fillna("Unknown")

    # ---------------------------------------------------------
    # Drop Unnecessary Columns
    # ---------------------------------------------------------

    def drop_columns(self):

        columns = []

        if "remarks" in self.df.columns:
            columns.append("remarks")

        if "sr_no" in self.df.columns:
            columns.append("sr_no")

        self.df.drop(columns=columns, inplace=True)

    # ---------------------------------------------------------
    # Dataset Summary
    # ---------------------------------------------------------

    def summary(self):

        print("\n----------------------------")
        print("Dataset Summary")
        print("----------------------------")

        print(self.df.info())

        print("\nMissing Values\n")

        print(self.df.isnull().sum())

        print("\nShape :", self.df.shape)

    # ---------------------------------------------------------
    # Save Dataset
    # ---------------------------------------------------------

    def save(self, path):

        self.df.to_csv(path, index=False)

        print(f"\nCleaned Dataset Saved -> {path}")

    # ---------------------------------------------------------
    # Complete Pipeline
    # ---------------------------------------------------------

    def run(self):

        self.load_data()

        self.rename_columns()

        self.remove_duplicates()

        self.clean_dates()

        self.clean_text()

        self.standardize_city()

        self.clean_amount()

        self.fill_missing()

        self.drop_columns()

        self.summary()

        return self.df


# =============================================================
# Main
# =============================================================

if __name__ == "__main__":

    processor = DataPreprocessor(
        "data/startup_funding.csv"
    )

    cleaned_df = processor.run()

    processor.save("data/cleaned_startup_funding.csv")