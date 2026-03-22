import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

hospitals = ["General Hospital Kollam", "District Hospital Ernakulam", "Taluk Hospital Thrissur"]
departments = ["General OPD", "Cardiology", "Orthopaedics", "Paediatrics", "Gynaecology"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

festival_dates = [
    "2024-01-26", "2024-03-25", "2024-04-14", "2024-08-15",
    "2024-09-07", "2024-10-02", "2024-10-12", "2024-10-31",
    "2024-11-01", "2024-11-15", "2024-12-25"
]

records = []

for _ in range(5000):
    hospital = random.choice(hospitals)
    department = random.choice(departments)
    day = random.choice(days)
    hour = random.randint(8, 17)
    month = random.randint(1, 12)
    is_weekend = 1 if day == "Saturday" else 0
    date_str = f"2024-{month:02d}-{random.randint(1,28):02d}"
    is_festival = 1 if date_str in festival_dates else 0

    # Simulate temperature (Kerala climate)
    temperature = round(random.uniform(24, 38), 1)
    is_rainy = 1 if (month in [6, 7, 8, 9] and random.random() < 0.6) else 0

    # Simulate patient count
    base_patients = random.randint(20, 80)
    if hour in [9, 10, 11]:
        base_patients += 30
    if is_festival:
        base_patients += 20
    if is_rainy:
        base_patients += 10
    if is_weekend:
        base_patients += 15

    # Wait time depends on patients + department complexity
    dept_factor = {"General OPD": 1.0, "Cardiology": 1.4, "Orthopaedics": 1.2,
                   "Paediatrics": 1.1, "Gynaecology": 1.3}
    wait_time = int(base_patients * dept_factor[department] * random.uniform(0.8, 1.2) / 3)
    wait_time = min(wait_time, 120)  # cap at 120 minutes

    records.append({
        "hospital": hospital,
        "department": department,
        "day_of_week": day,
        "hour": hour,
        "month": month,
        "is_weekend": is_weekend,
        "is_festival": is_festival,
        "temperature": temperature,
        "is_rainy": is_rainy,
        "patient_count": base_patients,
        "wait_time_minutes": wait_time
    })

df = pd.DataFrame(records)
df.to_csv("data/hospital_data.csv", index=False)
print(f"✅ Dataset created: {len(df)} rows")
print(df.head())