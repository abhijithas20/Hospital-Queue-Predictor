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

dept_base = {
    "General OPD": 35,
    "Cardiology": 55,
    "Orthopaedics": 45,
    "Paediatrics": 40,
    "Gynaecology": 50
}

records = []

for _ in range(8000):  # more data = better learning
    hospital   = random.choice(hospitals)
    department = random.choice(departments)
    day        = random.choice(days)
    hour       = random.randint(8, 17)
    month      = random.randint(1, 12)

    is_weekend = 1 if day == "Saturday" else 0
    date_str   = f"2024-{month:02d}-{random.randint(1,28):02d}"
    is_festival = 1 if date_str in festival_dates else 0

    temperature = round(random.uniform(24, 38), 1)
    is_rainy    = 1 if (month in [6, 7, 8, 9] and random.random() < 0.6) else 0

    # ── Wait time built directly from features ──────────────
    wait = dept_base[department]  # start with department base

    # Hour effect — morning rush 9–11, evening rush 4–5
    if hour in [9, 10, 11]:
        wait += 25
    elif hour in [16, 17]:
        wait += 15
    elif hour in [8, 12]:
        wait += 5
    else:
        wait -= 5

    # Day effect
    if day == "Monday":
        wait += 20   # busiest day
    elif day == "Saturday":
        wait += 15
    elif day in ["Wednesday", "Thursday"]:
        wait -= 10   # quietest days

    # Month effect — monsoon months busier
    if month in [6, 7, 8]:
        wait += 10

    # Festival & weather
    if is_festival:
        wait += 20
    if is_rainy:
        wait += 12
    if is_weekend:
        wait += 10

    # Small random noise (realistic variation)
    wait += random.randint(-8, 8)
    wait = max(5, min(wait, 120))  # keep between 5–120 min

    records.append({
        "hospital":          hospital,
        "department":        department,
        "day_of_week":       day,
        "hour":              hour,
        "month":             month,
        "is_weekend":        is_weekend,
        "is_festival":       is_festival,
        "temperature":       temperature,
        "is_rainy":          is_rainy,
        "wait_time_minutes": wait
    })

df = pd.DataFrame(records)
df.to_csv("data/hospital_data.csv", index=False)
print(f"✅ Dataset recreated: {len(df)} rows")
print(df.head())