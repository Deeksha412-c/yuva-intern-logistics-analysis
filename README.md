
# Week 1 — Strategic Planning and Data Exploration in Logistics

## Scenario
A hypothetical e-commerce warehouse needs to reduce stockouts and excess inventory through improved demand visibility and replenishment planning.

## KPIs
- Stockout rate = stockout observations / inventory observations × 100 (requires inventory availability data)
- Inventory turnover = cost of goods sold / average inventory value (requires cost and inventory records)
- Forecast accuracy: report MAE in units and optionally WAPE with zero-denominator handling
- Order fulfillment rate = fulfilled orders / total eligible orders × 100 (requires fulfillment records)

**Data limitation:** Transaction-only data cannot measure stockouts, turnover or fulfillment reliably without supplementary operational records.

## Research data
UCI Online Retail dataset: https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains sales transactions, not stock-on-hand or supplier lead times. Download the Excel file from UCI and place it at `data/Online Retail.xlsx` if you wish to explore actual transactions. It is not bundled here.

## Planned methodology
1. Define business questions, KPIs and data dictionary.
2. Collect transactions and, if available, inventory, fulfillment and lead-time records.
3. Clean dates, identifiers, returns and missing values.
4. Explore daily SKU demand and seasonality.
5. Compare a lag-one baseline against a regression model using chronological validation.
6. Calculate illustrative reorder points with documented assumptions.
7. Present limitations and business recommendations.

## Run illustration
From the repository root:

```bash
pip install -r week_1/requirements.txt
python week_1/src/data_exploration.py
python week_1/src/data_exploration.py --file "week_1/data/Online Retail.xlsx"
```

The default run uses clearly labeled synthetic observations. With a real Excel file, the script illustrates transaction cleaning, daily aggregation, and a naive demand forecast for one SKU. It is not a production model.

## Deliverables
- `report/strategic_planning_report.docx`: strategic planning document
- `src/data_exploration.py`: executable Python illustration
- `requirements.txt`: Python dependencies
- `data/README.md`: dataset provenance and access instructions

## References
- https://archive.ics.uci.edu/dataset/352/online+retail
- https://pandas.pydata.org/docs/
- https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

