from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import os
import csv
from datetime import datetime
from weather import get_weather

app = Flask(__name__)

# ── Load Model ────────────────────────────────────────────
def load_model():
    with open("model/model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ── Load Festival Dates ───────────────────────────────────
def load_festivals():
    df = pd.read_csv("data/festival_calendar.csv")
    return df["date"].tolist()

festival_dates = load_festivals()

# ── Encoding Maps ─────────────────────────────────────────
DAY_MAP = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2,
    "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 5
}
DEPT_MAP = {
    "General OPD": 0, "Cardiology": 1, "Orthopaedics": 2,
    "Paediatrics": 3, "Gynaecology": 4
}
HOSP_MAP = {
    "General Hospital Kollam": 0,
    "District Hospital Ernakulam": 1,
    "Taluk Hospital Thrissur": 2
}
CITY_MAP = {
    "General Hospital Kollam": "Kollam",
    "District Hospital Ernakulam": "Ernakulam",
    "Taluk Hospital Thrissur": "Thrissur"
}

# ── Routes ────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    hospital   = data["hospital"]
    department = data["department"]
    day_name   = data["day"]
    hour       = int(data["hour"])
    month      = int(data["month"])
    temperature = float(data["temperature"])
    is_rainy   = int(data["is_rainy"])
    date_str   = data["date"]

    is_festival = 1 if date_str in festival_dates else 0
    is_weekend  = 1 if day_name in ["Saturday", "Sunday"] else 0

    features = np.array([[
        HOSP_MAP.get(hospital, 0),
        DEPT_MAP.get(department, 0),
        DAY_MAP.get(day_name, 0),
        hour, month, is_weekend,
        is_festival, temperature, is_rainy
    ]])

    predicted = round(model.predict(features)[0])

    if predicted <= 20:
        level = "low"
    elif predicted <= 45:
        level = "moderate"
    else:
        level = "high"

    return jsonify({
        "wait_time": predicted,
        "level": level,
        "is_festival": is_festival,
        "day": day_name,
        "hour": hour
    })

@app.route("/weather", methods=["POST"])
def fetch_weather():
    data    = request.get_json()
    city    = CITY_MAP.get(data["hospital"], "Kollam")
    weather = get_weather(city)
    return jsonify(weather)

@app.route("/heatmap_data", methods=["POST"])
def heatmap_data():
    data       = request.get_json()
    hospital   = data["hospital"]
    department = data["department"]
    month      = int(data["month"])
    temperature = float(data["temperature"])
    is_rainy   = int(data["is_rainy"])
    is_festival = int(data["is_festival"])

    days  = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hours = list(range(8, 18))

    wait_matrix = []
    for day in days:
        row = []
        for hour in hours:
            is_weekend = 1 if day == "Saturday" else 0
            features = [[
                HOSP_MAP.get(hospital, 0),
                DEPT_MAP.get(department, 0),
                DAY_MAP.get(day, 0),
                hour, month, is_weekend,
                is_festival, temperature, is_rainy
            ]]
            pred = round(model.predict(features)[0])
            row.append(pred)
        wait_matrix.append(row)

    return jsonify({
        "days": days,
        "hours": [f"{h if h<=12 else h-12}{'AM' if h<12 else 'PM'}" for h in hours],
        "matrix": wait_matrix
    })

@app.route("/feedback", methods=["POST"])
def save_feedback():
    data = request.get_json()
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.exists("data/feedback.csv")
    with open("data/feedback.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "hospital", "department",
            "predicted", "actual", "accurate"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M"),
            "hospital":   data.get("hospital", ""),
            "department": data.get("department", ""),
            "predicted":  data.get("predicted", ""),
            "actual":     data.get("actual", ""),
            "accurate":   data.get("accurate", "")
        })
    return jsonify({"status": "saved"})

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)