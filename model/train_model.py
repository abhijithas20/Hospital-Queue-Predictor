import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# ── 1. Load Data ──────────────────────────────────────────
df = pd.read_csv("data/hospital_data_clean.csv")
print(f"✅ Data loaded: {df.shape[0]} rows")

# ── 2. Define Features & Target ───────────────────────────
# REPLACE THIS
features = [
    "hospital_encoded",
    "department_encoded",
    "day_encoded",
    "hour",
    "month",
    "is_weekend",
    "is_festival",
    "temperature",
    "is_rainy"
]

X = df[features]
y = df["wait_time_minutes"]

print(f"✅ Features selected: {features}")

# ── 3. Split into Train & Test ────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"✅ Train size: {len(X_train)} | Test size: {len(X_test)}")

# ── 4. Train the Model ────────────────────────────────────
print("\n⏳ Training Random Forest model...")
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
print("✅ Model trained!")

# ── 5. Evaluate the Model ─────────────────────────────────
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2  = r2_score(y_test, y_pred)

print("\n📊 Model Performance:")
print(f"   Mean Absolute Error : {mae:.2f} minutes")
print(f"   R² Score            : {r2:.4f}")

if r2 >= 0.85:
    print("   ✅ Excellent model!")
elif r2 >= 0.70:
    print("   ✅ Good model — acceptable for project!")
else:
    print("   ⚠️  Model needs improvement")

# ── 6. Feature Importance ─────────────────────────────────
print("\n🔍 Feature Importance:")
importances = model.feature_importances_
for feat, imp in sorted(zip(features, importances), key=lambda x: -x[1]):
    bar = "█" * int(imp * 50)
    print(f"   {feat:<25} {bar} {imp:.4f}")

# ── 7. Save the Model ─────────────────────────────────────
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n✅ Model saved to model/model.pkl")
print("🎉 Training complete!")