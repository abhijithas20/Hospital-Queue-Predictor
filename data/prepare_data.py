import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("data/hospital_data.csv")

print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\nColumn info:")
print(df.dtypes)

print("\nAny missing values?")
print(df.isnull().sum())

print("\nWait time stats:")
print(df["wait_time_minutes"].describe())

# Encode categorical columns
le = LabelEncoder()
df["hospital_encoded"] = le.fit_transform(df["hospital"])
df["department_encoded"] = le.fit_transform(df["department"])
df["day_encoded"] = le.fit_transform(df["day_of_week"])

# Save cleaned data
df.to_csv("data/hospital_data_clean.csv", index=False)
print("\n✅ Clean data saved to data/hospital_data_clean.csv")