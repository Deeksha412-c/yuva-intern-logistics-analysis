
"""
YuvaIntern - Week 2
Data Collection, Cleaning and Preprocessing
Project: E-Commerce Logistics Data Analysis
"""

from pathlib import Path
import pandas as pd

# ----------------------------------------
# STEP 1: Define file paths
# ----------------------------------------

BASE = Path(__file__).resolve().parents[1]

RAW_FILE = BASE / "data" / "raw_logistics.csv"
OUTPUT_FILE = BASE / "data" / "cleaned_logistics.csv"


def main():

    # ----------------------------------------
    # STEP 2: Load the dataset
    # ----------------------------------------

    df = pd.read_csv(RAW_FILE)

    print("=== RAW DATASET ===")
    print("Dataset shape:", df.shape)
    print(df.head())

    # ----------------------------------------
    # STEP 3: Identify missing values
    # ----------------------------------------

    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    # ----------------------------------------
    # STEP 4: Remove duplicate orders
    # ----------------------------------------

    df = df.drop_duplicates(
        subset=["Order_ID"],
        keep="first"
    ).copy()

    print("\nShape after duplicate removal:", df.shape)

    # ----------------------------------------
    # STEP 5: Clean text columns
    # ----------------------------------------

    for column in ["Product", "Region"]:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .str.title()
        )

    df["Product"] = df["Product"].fillna("Unknown")
    df["Region"] = df["Region"].fillna("Unknown")

    # ----------------------------------------
    # STEP 6: Convert date column
    # ----------------------------------------

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    # ----------------------------------------
    # STEP 7: Handle invalid numerical data
    # ----------------------------------------

    numerical_columns = [
        "Quantity",
        "Unit_Price",
        "Delivery_Days"
    ]

    for column in numerical_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        # Treat zero and negative values as invalid
        df.loc[df[column] <= 0, column] = float("nan")

        # Replace missing values with median
        median_value = df[column].median()

        if pd.isna(median_value):
            raise ValueError(
                f"No valid values in {column}"
            )

        df[column] = df[column].fillna(median_value)

    # Remove records with invalid dates
    df = df.dropna(
        subset=["Order_Date"]
    ).copy()

    # ----------------------------------------
    # STEP 8: Detect outliers using IQR
    # ----------------------------------------

    q1 = df["Quantity"].quantile(0.25)
    q3 = df["Quantity"].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    df["Quantity_Outlier"] = (
        (df["Quantity"] < lower_bound) |
        (df["Quantity"] > upper_bound)
    )

    print("\nQuantity outliers detected:")
    print(df["Quantity_Outlier"].sum())

    # ----------------------------------------
    # STEP 9: Min-Max Normalization
    # ----------------------------------------

    for column in numerical_columns:

        minimum = df[column].min()
        maximum = df[column].max()

        scaled_column = column + "_Scaled"

        if maximum > minimum:
            df[scaled_column] = (
                (df[column] - minimum) /
                (maximum - minimum)
            )
        else:
            df[scaled_column] = 0.0

    # ----------------------------------------
    # STEP 10: Calculate order value
    # ----------------------------------------

    df["Total_Value"] = (
        df["Quantity"] * df["Unit_Price"]
    )

    # ----------------------------------------
    # STEP 11: Validate cleaned dataset
    # ----------------------------------------

    print("\n=== CLEANED DATASET ===")
    print("Final shape:", df.shape)

    print("\nRemaining missing values:")
    print(df.isnull().sum())

    print("\nFirst five cleaned records:")
    print(df.head())

    # ----------------------------------------
    # STEP 12: Save cleaned dataset
    # ----------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        date_format="%Y-%m-%d"
    )

    print("\nPreprocessing completed successfully!")
    print("Cleaned file saved at:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
