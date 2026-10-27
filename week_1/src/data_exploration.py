"""Week 1: illustrative demand exploration and reorder-point calculation."""
import argparse
from pathlib import Path
import pandas as pd
from sklearn.metrics import mean_absolute_error


def load_daily_demand(file_path=None):
    if file_path is None:
        print("DEMO ONLY: using synthetic daily demand, not real logistics data.")
        return pd.DataFrame({
            "Date": pd.date_range("2026-01-01", periods=12, freq="D"),
            "Quantity": [10, 12, 9, 14, 11, 13, 12, 16, 14, 15, 13, 17],
        })
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path}")
    df = pd.read_excel(path)
    required = {"InvoiceNo", "InvoiceDate", "StockCode", "Quantity"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(df.columns))}")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate", "StockCode", "Quantity"])
    df = df[(df["Quantity"] > 0) & (~df["InvoiceNo"].astype(str).str.startswith("C"))]
    if df.empty:
        raise ValueError("No positive sales transactions remain after cleaning")
    sku = df["StockCode"].value_counts().index[0]
    print(f"Selected SKU: {sku}")
    subset = df.loc[df["StockCode"] == sku].copy()
    subset["Date"] = subset["InvoiceDate"].dt.normalize()
    daily = subset.groupby("Date")["Quantity"].sum().sort_index()
    # Missing days are assumed to have zero recorded sales, NOT zero underlying demand.
    daily = daily.asfreq("D", fill_value=0)
    return daily.rename("Quantity").reset_index()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Optional path to UCI Online Retail.xlsx")
    args = parser.parse_args()
    daily = load_daily_demand(args.file)
    daily["Prediction"] = daily["Quantity"].shift(1)
    valid = daily.dropna(subset=["Prediction"])
    print("Daily units (first 5 rows):")
    print(daily.head().to_string(index=False))
    if not valid.empty:
        # In-sample illustration only; a proper project needs chronological holdout.
        print(f"Illustrative lag-one MAE: {mean_absolute_error(valid['Quantity'], valid['Prediction']):.2f} units")
    avg_daily_demand = 12  # illustrative assumption, not an observed KPI
    lead_time_days = 5     # illustrative assumption
    safety_stock_units = 20  # illustrative assumption
    reorder_point = avg_daily_demand * lead_time_days + safety_stock_units
    print(f"Illustrative reorder point: {reorder_point} units")


if __name__ == "__main__":
    main()
