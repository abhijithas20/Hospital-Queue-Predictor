import pickle
import numpy as np

with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

# hospital, dept, day, hour, month, is_weekend, is_festival, temp, is_rainy, patient_count
test_input = np.array([[0, 0, 0, 10, 6, 0, 0, 30.0, 0, 40]])
prediction = model.predict(test_input)[0]
print(f"🏥 Predicted wait time: {round(prediction)} minutes")

test_festival = np.array([[0, 0, 0, 10, 9, 0, 1, 28.0, 1, 65]])
prediction_festival = model.predict(test_festival)[0]
print(f"🎉 Predicted wait time on festival+rain day: {round(prediction_festival)} minutes")