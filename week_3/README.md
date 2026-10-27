# YuvaIntern Week 3 — Advanced Logistics Data Analysis and Visualization

## Project overview
This project continues Week 2's **synthetic** cleaned e-commerce logistics records. It performs exploratory data analysis (EDA), computes descriptive statistics and correlations, and generates six PNG charts. Transportation costs are **simulated** using documented assumptions; they are not actual carrier charges.

## Folder structure
```
week_3/
├── README.md
├── requirements.txt
├── src/analyze_logistics.py
├── data/week2_cleaned_logistics.csv
├── data/week3_analysis_dataset.csv
├── data/descriptive_statistics.csv
├── data/regional_summary.csv
├── data/correlations.csv
├── visualizations/*.png
└── report/week_3_logistics_eda_report.docx
```

## Run
From the `week_3` folder:
```bash
python -m pip install -r requirements.txt
python src/analyze_logistics.py
```
Paths are resolved relative to the script, so this also works from the repository root.

## Dataset and definitions
Source: synthetic Week 2 cleaned dataset, 79 orders. `Shipment_Volume` is units ordered, not packages. `Order_Value` = Quantity × Unit_Price. `Transport_Cost_Simulated` = (80 + 12 × units + 18 × delivery days) × region factor (North 1.15, South 1.00, East 1.10, West 1.05). Currency is deliberately unspecified; values are illustrative cost units. `Delivery_On_Time_Proxy` is delivery days ≤4, not actual SLA compliance.

## Key results
- 79 orders; 449 units; mean delivery time 4.23 days; median 3 days.
- 58.23% of orders delivered within an illustrative four-day threshold.
- West has the highest mean delivery time (4.73 days).
- South has the largest total shipment volume (204 units).
- Average simulated transportation cost: 240.15 illustrative units.
- Volume vs simulated cost correlation: 0.960; this strong correlation is expected because volume is part of the cost formula, and must not be interpreted as empirical causal evidence.

## Visualizations
1. Delivery time histogram: delivery-time distribution.
2. Regional shipment bar chart: volume differences.
3. Regional delivery boxplot: spread and possible bottlenecks.
4. Volume vs simulated cost scatter: formula-driven relationship.
5. Correlation heatmap: numerical associations.
6. Monthly shipment line plot: time aggregation; short date range prevents reliable seasonality claims.

## Limitations
The data is hypothetical and small; costs and four-day threshold are assumptions. Outlier quantities from Week 2 remain for transparency. Findings are demonstrations, not verified operational conclusions. Do not use the dataset to claim real-world performance.
