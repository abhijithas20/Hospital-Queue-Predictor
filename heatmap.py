import plotly.graph_objects as go
import numpy as np

def generate_heatmap(hospital, department, month, model, temperature, is_rainy, is_festival):

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hours = list(range(8, 18))  # 8AM to 5PM

    day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2,
               "Thursday": 3, "Friday": 4, "Saturday": 5}
    dept_map = {"General OPD": 0, "Cardiology": 1, "Orthopaedics": 2,
                "Paediatrics": 3, "Gynaecology": 4}
    hospital_map = {"General Hospital Kollam": 0,
                    "District Hospital Ernakulam": 1,
                    "Taluk Hospital Thrissur": 2}

    # Build wait time grid
    wait_matrix = []
    for day in days:
        row = []
        for hour in hours:
            is_weekend = 1 if day == "Saturday" else 0
            features = [[
                hospital_map.get(hospital, 0),
                dept_map.get(department, 0),
                day_map.get(day, 0),
                hour,
                month,
                is_weekend,
                is_festival,
                temperature,
                is_rainy
            ]]
            pred = model.predict(features)[0]
            row.append(round(pred))
        wait_matrix.append(row)

    hour_labels = [f"{h}:00" for h in hours]

    fig = go.Figure(data=go.Heatmap(
        z=wait_matrix,
        x=hour_labels,
        y=days,
        colorscale=[
            [0.0,  "#2ecc71"],   # Green  — short wait
            [0.5,  "#f39c12"],   # Yellow — moderate
            [1.0,  "#e74c3c"]    # Red    — long wait
        ],
        colorbar=dict(
            title="Wait (min)",
            tickvals=[10, 30, 60, 90],
            ticktext=["10 min", "30 min", "60 min", "90 min"]
        ),
        hovertemplate="<b>%{y}</b> at <b>%{x}</b><br>Wait: %{z} minutes<extra></extra>"
    ))

    fig.update_layout(
        title=f"⏱️ Weekly Wait Time Heatmap — {department}",
        xaxis_title="Hour of Day",
        yaxis_title="Day of Week",
        font=dict(size=13),
        height=420
    )

    return fig, wait_matrix, days, hours