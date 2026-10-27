# YuvaIntern Week 4 — Predictive Modeling and Optimization in Logistics

Forecast delivery duration from simulated e-commerce orders. This folder continues the Week 1–3 project.

## Contents
- `src/model_delivery.py`: end-to-end forecasting, cross-validation, evaluation, dispatch review scenario
- `data/week3_analysis_dataset.csv`: 79-row synthetic dataset reused from Week 3
- `report/week_4_predictive_modeling_report.docx`: submission report
- `report/model_metrics.csv`: comparison of three models
- `report/dispatch_priority_scenario.csv`: five review flags on held-out records
- `report/run_summary.json`: data split and selected model
- `visualizations/`: test-error comparison and actual-vs-predicted plots

## Run
```bash
cd week_4
python -m pip install -r requirements.txt
python src/model_delivery.py
```

## Method
Predict `Delivery_Days` using only order-time information: Quantity, Unit_Price, Region, Product, month and weekday. Chronological 80/20 split; TimeSeriesSplit(3) on training set. Compare mean baseline, ridge regression and random forest. Select using CV MAE, report untouched test MAE/RMSE/R². Preprocessing is fitted inside CV pipelines.

## Findings
79 records; 63 train, 16 test. Random forest has best training CV MAE (2.409 days) but test MAE 2.588 days, worse than mean baseline (2.500 days). No evidence of production-grade predictive accuracy. The five-order expedite-review scenario is illustrative and does **not** establish delivery improvements or cost savings.

## Data limitations
Data are simulated and small. `Transport_Cost_Simulated`, `Delivery_On_Time_Proxy`, and `Delivery_Days_Scaled` are excluded to prevent target leakage. Do not generalize findings to real logistics operations.
