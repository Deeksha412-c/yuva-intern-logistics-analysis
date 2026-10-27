"""YuvaIntern Week 4: leakage-aware delivery-time forecasting and capacity scenarios."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'week3_analysis_dataset.csv'
REPORT = ROOT / 'report'
VIS = ROOT / 'visualizations'
REPORT.mkdir(exist_ok=True)
VIS.mkdir(exist_ok=True)

raw = pd.read_csv(DATA, parse_dates=['Order_Date'])
raw = raw.dropna(subset=['Order_Date', 'Delivery_Days']).sort_values(['Order_Date', 'Order_ID']).reset_index(drop=True)
# Only variables assumed available when the order is placed. Never include
# Delivery_Days_Scaled, Delivery_On_Time_Proxy or simulated transport cost.
features = ['Quantity', 'Unit_Price', 'Region', 'Product', 'Order_Month', 'Order_DayOfWeek']
raw['Order_Month'] = raw['Order_Date'].dt.month
raw['Order_DayOfWeek'] = raw['Order_Date'].dt.dayofweek
X, y = raw[features], raw['Delivery_Days'].astype(float)
num = ['Quantity', 'Unit_Price', 'Order_Month', 'Order_DayOfWeek']
cat = ['Region', 'Product']
prep = ColumnTransformer([
 ('numeric', Pipeline([('impute', SimpleImputer(strategy='median')), ('scale', StandardScaler())]), num),
 ('category', Pipeline([('impute', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore'))]), cat)
])
models = {
 'Mean baseline': DummyRegressor(strategy='mean'),
 'Ridge regression': Ridge(alpha=10.0),
 'Random forest': RandomForestRegressor(n_estimators=120, min_samples_leaf=4, max_depth=5, random_state=42)
}
cut = int(len(raw)*0.8)
X_train, X_test = X.iloc[:cut], X.iloc[cut:]
y_train, y_test = y.iloc[:cut], y.iloc[cut:]
results, fitted, preds = [], {}, {}
for name, estimator in models.items():
 model = Pipeline([('preprocess', prep), ('model', estimator)])
 cv = TimeSeriesSplit(n_splits=3)
 cv_mae = -cross_val_score(model, X_train, y_train, cv=cv, scoring='neg_mean_absolute_error')
 model.fit(X_train, y_train)
 pred = model.predict(X_test)
 results.append({'model':name, 'cv_mae_mean':round(float(cv_mae.mean()),3), 'cv_mae_std':round(float(cv_mae.std()),3),
  'test_mae':round(float(mean_absolute_error(y_test,pred)),3),
  'test_rmse':round(float(np.sqrt(mean_squared_error(y_test,pred))),3),
  'test_r2':round(float(r2_score(y_test,pred)),3)})
 fitted[name], preds[name] = model, pred
# Select on training-only CV; do not select using the test set.
chosen = min(results, key=lambda r:r['cv_mae_mean'])['model']
result_df = pd.DataFrame(results)
result_df.to_csv(REPORT/'model_metrics.csv', index=False)
print(result_df.to_string(index=False))
print('CV-selected model:', chosen)

fig,ax=plt.subplots(figsize=(8,4.5))
xx=np.arange(len(results)); ax.bar(xx,[r['test_mae'] for r in results]);ax.set_xticks(xx,[r['model'] for r in results],rotation=12)
ax.set_ylabel('Test MAE (days)');ax.set_title('Held-out forecast error (lower is better)');fig.tight_layout();fig.savefig(VIS/'model_comparison.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(7,5));ax.scatter(y_test,preds[chosen],alpha=.8);lo=min(y_test.min(),np.min(preds[chosen]));hi=max(y_test.max(),np.max(preds[chosen]));ax.plot([lo,hi],[lo,hi],linestyle='--',color='gray');ax.set(xlabel='Actual delivery days',ylabel='Predicted delivery days',title='Held-out predictions: '+chosen);fig.tight_layout();fig.savefig(VIS/'actual_vs_predicted.png',dpi=160);plt.close(fig)

# Illustrative allocation rule: 5 slots for extra dispatch attention; this is
# NOT an optimized routing solution or a measured improvement in delivery time.
priority = raw.iloc[cut:][['Order_ID','Region','Quantity','Delivery_Days']].copy()
priority['Predicted_Delivery_Days'] = np.maximum(preds[chosen],0)
priority['Priority_Rank'] = priority['Predicted_Delivery_Days'].rank(method='first',ascending=False).astype(int)
priority['Allocate_Expedite_Review'] = priority['Priority_Rank'] <= min(5,len(priority))
priority.sort_values('Priority_Rank').to_csv(REPORT/'dispatch_priority_scenario.csv',index=False)
summary={'records':len(raw),'train_records':len(X_train),'test_records':len(X_test),'chosen_by_cv':chosen,'scenario_review_slots':min(5,len(priority)), 'notes':'Synthetic demonstration; capacity allocation is illustrative, not proven to reduce cost or delivery time.'}
(REPORT/'run_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
