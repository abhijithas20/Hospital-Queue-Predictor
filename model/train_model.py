import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import json

# ── Load Data ─────────────────────────────────────────────
df = pd.read_csv("data/hospital_data_clean.csv")
print(f"✅ Data loaded: {df.shape[0]} rows")

features = [
    "hospital_encoded", "department_encoded", "day_encoded",
    "hour", "month", "is_weekend", "is_festival",
    "temperature", "is_rainy"
]

X = df[features]
y = df["wait_time_minutes"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Train All 3 Models ────────────────────────────────────
models = {
    "Random Forest":   RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    "Decision Tree":   DecisionTreeRegressor(max_depth=10, random_state=42),
    "Linear Regression": LinearRegression()
}

results = {}

for name, m in models.items():
    print(f"\n⏳ Training {name}...")
    m.fit(X_train, y_train)
    y_pred = m.predict(X_test)
    mae = round(mean_absolute_error(y_test, y_pred), 2)
    r2  = round(r2_score(y_test, y_pred), 4)
    results[name] = {"mae": mae, "r2": r2}
    print(f"   R² : {r2}  |  MAE : {mae} min")

# ── Save Best Model (Random Forest) ──────────────────────
with open("model/model.pkl", "wb") as f:
    pickle.dump(models["Random Forest"], f)
print("\n✅ Best model (Random Forest) saved to model/model.pkl")

# ── Save Comparison Results ───────────────────────────────
with open("model/comparison.json", "w") as f:
    json.dump(results, f)
print("✅ Comparison results saved to model/comparison.json")

print("\n🎉 All done!")