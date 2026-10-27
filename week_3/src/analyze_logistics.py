"""YuvaIntern Week 3: reproducible EDA using Week 2 cleaned synthetic orders.
Transportation cost is SIMULATED and is not an observed company cost.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data'
FIG = BASE / 'visualizations'
FIG.mkdir(exist_ok=True)
sns.set_theme(style='whitegrid', palette='deep')


def main():
    df = pd.read_csv(DATA / 'week2_cleaned_logistics.csv', parse_dates=['Order_Date'])
    required = {'Order_ID', 'Order_Date', 'Product', 'Quantity', 'Unit_Price', 'Region', 'Delivery_Days'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    df = df.dropna(subset=list(required)).copy()
    for col in ['Quantity', 'Unit_Price', 'Delivery_Days']:
        df[col] = pd.to_numeric(df[col], errors='raise')
    if (df[['Quantity', 'Unit_Price', 'Delivery_Days']] < 0).any().any():
        raise ValueError('Negative numeric values require investigation')
    df['Shipment_Volume'] = df['Quantity']  # units per order, not number of parcels
    df['Order_Value'] = df['Quantity'] * df['Unit_Price']
    # Illustrative scenario assumption: fixed dispatch fee + per-unit fee + per-day fee
    # plus region multiplier. This is NOT real observed transportation cost.
    region_factor = {'North': 1.15, 'South': 1.00, 'East': 1.10, 'West': 1.05}
    df['Transport_Cost_Simulated'] = (
        80 + 12 * df['Shipment_Volume'] + 18 * df['Delivery_Days']
    ) * df['Region'].map(region_factor).fillna(1.0)
    df['Delivery_On_Time_Proxy'] = df['Delivery_Days'] <= 4  # assumption, no promised date
    df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)
    df.to_csv(DATA / 'week3_analysis_dataset.csv', index=False)

    metrics = {
        'orders': len(df), 'total_units': int(df['Shipment_Volume'].sum()),
        'mean_delivery_days': round(df['Delivery_Days'].mean(), 2),
        'median_delivery_days': round(df['Delivery_Days'].median(), 2),
        'mean_simulated_transport_cost': round(df['Transport_Cost_Simulated'].mean(), 2),
        'total_simulated_transport_cost': round(df['Transport_Cost_Simulated'].sum(), 2),
        'proxy_within_4_days_pct': round(df['Delivery_On_Time_Proxy'].mean() * 100, 2),
        'total_order_value': round(df['Order_Value'].sum(), 2),
    }
    print('KEY METRICS')
    for key, val in metrics.items():
        print(f'{key}: {val}')
    (BASE / 'report' / 'metrics.txt').write_text('\n'.join(f'{k}: {v}' for k, v in metrics.items())+'\n', encoding='utf-8')
    summary = df[['Shipment_Volume', 'Delivery_Days', 'Transport_Cost_Simulated', 'Order_Value']].describe().round(2)
    summary.to_csv(DATA / 'descriptive_statistics.csv')
    region = df.groupby('Region').agg(Orders=('Order_ID', 'count'), Units=('Shipment_Volume', 'sum'), Mean_Delivery_Days=('Delivery_Days', 'mean'), Mean_Simulated_Cost=('Transport_Cost_Simulated', 'mean')).round(2)
    region.to_csv(DATA / 'regional_summary.csv')
    correlations = df[['Shipment_Volume', 'Delivery_Days', 'Transport_Cost_Simulated', 'Order_Value']].corr().round(3)
    correlations.to_csv(DATA / 'correlations.csv')
    print('\nREGIONAL SUMMARY\n', region)
    print('\nCORRELATIONS\n', correlations)

    plt.figure(figsize=(8, 5))
    plt.hist(df['Delivery_Days'], bins=np.arange(df['Delivery_Days'].min() - .5, df['Delivery_Days'].max() + 1.5, 1), edgecolor='white')
    plt.title('Delivery time distribution'); plt.xlabel('Delivery days'); plt.ylabel('Orders')
    plt.tight_layout(); plt.savefig(FIG / 'delivery_time_distribution.png', dpi=180); plt.close()

    plt.figure(figsize=(8, 5))
    region['Units'].sort_values(ascending=False).plot(kind='bar')
    plt.title('Shipment volume by region'); plt.xlabel('Region'); plt.ylabel('Units ordered')
    plt.xticks(rotation=0); plt.tight_layout(); plt.savefig(FIG / 'shipment_volume_by_region.png', dpi=180); plt.close()

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='Region', y='Delivery_Days', order=sorted(df['Region'].unique()))
    plt.title('Delivery time variability by region'); plt.ylabel('Delivery days')
    plt.tight_layout(); plt.savefig(FIG / 'delivery_days_by_region.png', dpi=180); plt.close()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='Shipment_Volume', y='Transport_Cost_Simulated', hue='Region', alpha=.75)
    plt.title('Simulated transportation cost vs shipment volume'); plt.xlabel('Units per order'); plt.ylabel('Simulated cost (illustrative units)')
    plt.tight_layout(); plt.savefig(FIG / 'cost_vs_volume.png', dpi=180); plt.close()

    plt.figure(figsize=(7, 5))
    sns.heatmap(correlations, annot=True, cmap='coolwarm', center=0, vmin=-1, vmax=1, fmt='.2f')
    plt.title('Correlation of key metrics'); plt.tight_layout(); plt.savefig(FIG / 'correlation_heatmap.png', dpi=180); plt.close()

    monthly = df.groupby('Month')['Shipment_Volume'].sum()
    plt.figure(figsize=(8, 5))
    monthly.plot(marker='o'); plt.title('Monthly shipment volume'); plt.xlabel('Order month'); plt.ylabel('Units ordered')
    plt.tight_layout(); plt.savefig(FIG / 'monthly_shipment_volume.png', dpi=180); plt.close()
    print('\nSaved six visualizations and summary CSV files.')


if __name__ == '__main__':
    main()
