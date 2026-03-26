import streamlit as st
import pickle
import numpy as np
import pandas as pd
import sys
import os

# Path fix so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather import get_weather
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'charts'))
from heatmap import generate_heatmap

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Hospital Wait Time Predictor",
    page_icon="🏥",
    layout="wide"
)

# ── Auto Train if model.pkl missing ───────────────────────
def train_if_missing():
    if not os.path.exists("model/model.pkl"):
        st.info("⏳ First run detected — training model, please wait...")
        import subprocess
        subprocess.run(["python", "data/generate_data.py"])
        subprocess.run(["python", "data/prepare_data.py"])
        subprocess.run(["python", "model/train_model.py"])
        st.success("✅ Model trained successfully!")
        st.rerun()

train_if_missing()

# ── Load Model ────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("model/model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ── Load Festival Data ────────────────────────────────────
@st.cache_data
def load_festivals():
    df = pd.read_csv("data/festival_calendar.csv")
    return df["date"].tolist()

festival_dates = load_festivals()

# ── Header ────────────────────────────────────────────────
st.title("🏥 Hospital OPD Wait Time Predictor")
st.markdown("*Predict waiting times at Indian government hospitals before you visit*")
st.divider()

# ── Sidebar Inputs ────────────────────────────────────────
st.sidebar.header("🔧 Select Your Visit Details")

hospital = st.sidebar.selectbox("🏨 Hospital", [
    "General Hospital Kollam",
    "District Hospital Ernakulam",
    "Taluk Hospital Thrissur"
])

department = st.sidebar.selectbox("🩺 Department", [
    "General OPD",
    "Cardiology",
    "Orthopaedics",
    "Paediatrics",
    "Gynaecology"
])

visit_date = st.sidebar.date_input("📅 Visit Date")

hour = st.sidebar.slider("🕐 Arrival Time (Hour)", 8, 17, 10)
st.sidebar.caption(f"Selected: {hour}:00")

st.sidebar.divider()

# ── Weather (Auto-fetch) ───────────────────────────────────
city_map = {
    "General Hospital Kollam": "Kollam",
    "District Hospital Ernakulam": "Ernakulam",
    "Taluk Hospital Thrissur": "Thrissur"
}

with st.sidebar:
    st.subheader("🌦️ Live Weather")
    if st.button("Fetch Live Weather"):
        weather = get_weather(city_map[hospital])
        st.session_state["weather"] = weather

    if "weather" not in st.session_state:
        st.session_state["weather"] = {"temperature": 30.0, "is_rainy": 0, "weather_description": "Default"}

    w = st.session_state["weather"]
    st.metric("🌡️ Temperature", f"{w['temperature']} °C")
    st.metric("🌧️ Condition", w["weather_description"])

# ── Festival Check ────────────────────────────────────────
date_str = str(visit_date)
is_festival = 1 if date_str in festival_dates else 0
month = visit_date.month

if is_festival:
    st.sidebar.warning("🎉 Festival day detected — expect higher wait times!")

# ── Predict Button ────────────────────────────────────────
st.subheader("📊 Your Predicted Wait Time")

day_name = visit_date.strftime("%A")

day_map  = {"Monday": 0, "Tuesday": 1, "Wednesday": 2,
            "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 5}
dept_map = {"General OPD": 0, "Cardiology": 1, "Orthopaedics": 2,
            "Paediatrics": 3, "Gynaecology": 4}
hosp_map = {"General Hospital Kollam": 0,
            "District Hospital Ernakulam": 1,
            "Taluk Hospital Thrissur": 2}

is_weekend = 1 if day_name in ["Saturday", "Sunday"] else 0
w = st.session_state["weather"]

features = np.array([[
    hosp_map.get(hospital, 0),
    dept_map.get(department, 0),
    day_map.get(day_name, 0),
    hour,
    month,
    is_weekend,
    is_festival,
    w["temperature"],
    w["is_rainy"]
]])

predicted = round(model.predict(features)[0])

# Colour-coded result
col1, col2, col3 = st.columns(3)

with col1:
    if predicted <= 20:
        st.success(f"🟢 **{predicted} minutes**\nShort wait — great time to visit!")
    elif predicted <= 45:
        st.warning(f"🟡 **{predicted} minutes**\nModerate wait — plan accordingly.")
    else:
        st.error(f"🔴 **{predicted} minutes**\nLong wait — consider a different time.")

with col2:
    st.info(f"📅 **{day_name}** at **{hour}:00**")

with col3:
    if is_festival:
        st.warning("🎉 Festival Day")
    elif w["is_rainy"]:
        st.info("🌧️ Rainy Day")
    else:
        st.success("☀️ Normal Day")

st.divider()

# ── Heatmap ───────────────────────────────────────────────
st.subheader("🗓️ Weekly Wait Time Heatmap")
st.caption("Green = short wait · Yellow = moderate · Red = long wait")

fig, wait_matrix, days, hours = generate_heatmap(
    hospital, department, month, model,
    w["temperature"], w["is_rainy"], is_festival
)
st.plotly_chart(fig, use_container_width=True)

# ── Best Time Recommendation ──────────────────────────────
st.subheader("💡 Best Time to Visit")

col_week, col_day = st.columns(2)

# ── Best time in the whole week ───────────────────────────
best_wait_week = 999
best_day_week  = ""
best_hour_week = 0

for i, day in enumerate(days):
    for j, h in enumerate(range(8, 18)):
        if wait_matrix[i][j] < best_wait_week:
            best_wait_week = wait_matrix[i][j]
            best_day_week  = day
            best_hour_week = h

with col_week:
    st.markdown("#### 📅 Best Time This Week")
    st.success(
        f"**{best_day_week}** at **{best_hour_week}:00**\n\n"
        f"~{best_wait_week} min wait"
    )

# ── Best time on the user's selected day ─────────────────
day_index = days.index(day_name) if day_name in days else 0

best_wait_day  = 999
best_hour_day  = 0

for j, h in enumerate(range(8, 18)):
    if wait_matrix[day_index][j] < best_wait_day:
        best_wait_day  = wait_matrix[day_index][j]
        best_hour_day  = h

with col_day:
    st.markdown(f"#### 🕐 Best Time on {day_name}")
    if best_wait_day <= 20:
        st.success(
            f"Visit at **{best_hour_day}:00**\n\n"
            f"~{best_wait_day} min wait 🟢"
        )
    elif best_wait_day <= 45:
        st.warning(
            f"Visit at **{best_hour_day}:00**\n\n"
            f"~{best_wait_day} min wait 🟡"
        )
    else:
        st.error(
            f"Visit at **{best_hour_day}:00**\n\n"
            f"~{best_wait_day} min wait 🔴"
        )
    st.caption(f"For {department} on {day_name}")

st.divider()
st.caption("Built by Abhijith AS | IZee Business School | BCA Final Year Project 2026")