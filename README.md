# 🏥 Hospital OPD Wait Time Predictor

A machine learning web app that predicts OPD waiting times at Indian government hospitals — built as a Final Year BCA Project.

---

## 🌐 Live Demo
> Deployed on Streamlit Cloud — link coming soon

---

## 📌 What It Does

- Predicts OPD wait time based on hospital, department, day, and hour
- Integrates **real-time weather** via OpenWeatherMap API
- Detects **Indian festival days** (Onam, Diwali, Vishu etc.) and adjusts predictions
- Displays a **colour-coded weekly heatmap** (🟢 Low / 🟡 Moderate / 🔴 High)
- Shows **best time to visit** — both for the selected day and the whole week

---

## 🧠 ML Model

| Detail | Value |
|---|---|
| Algorithm | Random Forest Regressor |
| Training Rows | 8,000 |
| Features | 9 (hour, day, department, weather, festival etc.) |
| R² Score | 0.9254 |
| MAE | ~4 minutes |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| ML Model | Scikit-learn (Random Forest) |
| Data | Pandas, NumPy |
| Visualisation | Plotly |
| Web UI | Streamlit |
| Weather | OpenWeatherMap API |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure
```
hospital-queue-predictor/
├── data/
│   ├── generate_data.py
│   ├── prepare_data.py
│   ├── hospital_data.csv
│   ├── hospital_data_clean.csv
│   ├── festival_calendar.csv
│   └── hospitals_list.csv
├── model/
│   ├── train_model.py
│   └── model.pkl (auto-generated on first run)
├── app/
│   ├── app.py
│   ├── predict.py
│   └── weather.py
├── charts/
│   └── heatmap.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Run Locally
```bash
git clone https://github.com/abhijithas20/Hospital-Queue-Predictor.git
cd Hospital-Queue-Predictor
pip install -r requirements.txt
streamlit run app/app.py
```

---

## 👨‍💻 Developer

**Abhijith AS**
BCA Final Year | AI & ML Specialisation
IZee Business School | 2023–2026
Register Number: U03EX23S0047