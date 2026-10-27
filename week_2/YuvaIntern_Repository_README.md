# YuvaIntern — Logistics Data Analytics Internship

A Python-based learning repository documenting weekly logistics analytics assignments, from strategic planning to data preprocessing. The case study focuses on inventory and order data for a hypothetical e-commerce retailer.

> **Project scope:** The examples use simulated data. They do not represent a real company's operations, and no production forecasting model has been trained.

## Project objectives

- Identify inventory and fulfillment performance indicators.
- Design a practical workflow for collecting and exploring logistics data.
- Clean and validate order records before analysis.
- Detect unusual values and prepare numeric features for later modeling.
- Document methods, assumptions, and limitations in Word reports.

## Repository structure

```text
yuva-intern-logistics-analysis/
├── README.md
├── week_1/
│   ├── README.md
│   ├── requirements.txt
│   ├── src/
│   │   └── data_exploration.py
│   ├── data/
│   │   └── README.md
│   └── report/
│       └── strategic_planning_report.docx
└── week_2/
    ├── README.md
    ├── requirements.txt
    ├── src/
    │   └── preprocess.py
    ├── data/
    │   ├── README.md
    │   ├── raw_logistics.csv
    │   └── cleaned_logistics.csv
    └── report/
        └── week_2_preprocessing_report.docx
```

## Week 1 — Strategic Planning and Data Exploration

**Topic:** Optimizing E-Commerce Inventory and Supply Chain Efficiency Using Python.

This planning assignment describes a hypothetical logistics challenge, defines KPIs (stockout rate, inventory turnover, forecast accuracy, and order fulfillment rate), reviews potential public data sources, and proposes an end-to-end analytical roadmap. It includes an illustrative Python exploration script; it is not a completed forecasting model.

- Report: [`week_1/report/strategic_planning_report.docx`](week_1/report/strategic_planning_report.docx)
- Code: [`week_1/src/data_exploration.py`](week_1/src/data_exploration.py)
- Details: [`week_1/README.md`](week_1/README.md)

## Week 2 — Data Collection, Cleaning, and Preprocessing

**Topic:** Preparing simulated e-commerce logistics records for analysis.

The preprocessing script:

1. Loads a synthetic CSV and reports missing values.
2. Removes repeated order IDs, retaining the first occurrence.
3. Standardizes product and region labels and parses order dates.
4. Converts numeric columns and replaces missing or nonpositive values using column medians.
5. Removes records with invalid dates.
6. Flags quantity outliers using the interquartile range (IQR) rule without automatically deleting them.
7. Adds min-max scaled numerical features and calculates total order value.
8. Exports a cleaned CSV and prints a summary.

- Report: [`week_2/report/week_2_preprocessing_report.docx`](week_2/report/week_2_preprocessing_report.docx)
- Code: [`week_2/src/preprocess.py`](week_2/src/preprocess.py)
- Raw data: [`week_2/data/raw_logistics.csv`](week_2/data/raw_logistics.csv)
- Cleaned data: [`week_2/data/cleaned_logistics.csv`](week_2/data/cleaned_logistics.csv)
- Details: [`week_2/README.md`](week_2/README.md)

## Requirements

- Python 3.10 or later
- `pandas` for Week 2 (see each week's `requirements.txt` for the complete dependency list)

## Run locally

From the **repository root** in Git Bash:

```bash
python -m pip install -r week_1/requirements.txt
python week_1/src/data_exploration.py

python -m pip install -r week_2/requirements.txt
python week_2/src/preprocess.py
```

The Week 2 script locates its data files relative to its own location, so it can be run from the repository root. It overwrites `week_2/data/cleaned_logistics.csv` with the generated output.

## Dataset provenance and limitations

Week 2 uses **synthetic records with intentionally introduced quality issues** for educational demonstration. The UCI Online Retail dataset is a possible public reference for future real-data exploration, but it is not the source of these synthetic records: https://archive.ics.uci.edu/dataset/352/online+retail

The Week 2 pipeline is a demonstration rather than a production preprocessing system. Median imputation can distort distributions, repeated IDs require business-rule validation, and min-max scaling must be fitted on training data only when developing predictive models to avoid data leakage.

## Submission

Each week has its own Word report and supporting code. The same GitHub repository URL can be submitted for both weeks if YuvaIntern accepts a multi-week repository. Confirm that the relevant weekly files have been pushed and are visible before submitting.
