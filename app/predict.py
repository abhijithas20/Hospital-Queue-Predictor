import pickle
import numpy as np
import pandas as pd

def load_model():
    with open("model/model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

def predict_wait_time(hospital, department, day, hour, month, temperature, is_rainy, is_festival):
    
    day_map = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2,
        "Thursday": 3, "Friday": 4, "Saturday": 5
    }
    dept_map = {
        "General OPD": 0, "Cardiology": 1, "Orthopaedics": 2,
        "Paediatrics": 3, "Gynaecology": 4
    }
    hospital_map = {
        "General Hospital Kollam": 0,
        "District Hospital Ernakulam": 1,
        "Taluk Hospital Thrissur": 2
    }

    is_weekend = 1 if day == "Saturday" else 0

    features = np.array([[
        hospital_map.get(hospital, 0),
        dept_map.get(department, 0),
        day_map.get(day, 0),
        hour,
        month,
        is_weekend,
        is_festival,
        temperature,
        is_rainy
    ]])

    model = load_model()
    prediction = model.predict(features)[0]
    return round(prediction)