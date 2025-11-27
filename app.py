from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json

app = FastAPI()

# Mapping: label -> class number
LABEL_TO_CLASS = {
    "Flow Instability": 1,
    "Pressure Anomaly": 2,
    "Chemical Composition": 3,
    "Temperature Anomaly": 4,
    "Fluid Level Anomaly": 5,
    "Viscosity Anomaly": 6
}

# Colors for each anomaly label
LABEL_COLORS = {
    "Flow Instability": "#ff3b30",
    "Pressure Anomaly": "#ff3b30",
    "Chemical Composition": "#ffcc00",
    "Temperature Anomaly": "#34c759",
    "Fluid Level Anomaly": "#34c759",
    "Viscosity Anomaly": "#34c759"
}

class AIItem(BaseModel):
    label: str
    timestamp: str  # ISO 8601 format (e.g., 2023-05-01T12:32:00)

class RequestModel(BaseModel):
    ai_items: list[AIItem]


@app.get("/")
def root():
    return {"message": "Failure Prediction API is running. Use /predict (POST) to get predictions."}


@app.post("/predict")
def predict(req: RequestModel):
    with open("MData.json", "r") as f:
        sensor_data = json.load(f)

    events = []
    for item in req.ai_items:
        events.append({
            "label": item.label,
            "class": LABEL_TO_CLASS.get(item.label, 0),
            "color": LABEL_COLORS.get(item.label, "#000000"),
            "timestamp": datetime.fromisoformat(item.timestamp)
        })

    output_items = []

    for row in sensor_data:
        t = row["Timesteap"]

        try:
            row_time = datetime.strptime(t, "%H:%M:%S")
        except:
            row_time = datetime.strptime(t, " day1 %I:%M:%S %p")

        assigned_label = "Normal"
        assigned_class = 0
        assigned_color = "#ffffff"

        for e in events:
            if row_time.hour == e["timestamp"].hour and abs(row_time.minute - e["timestamp"].minute) < 2:
                assigned_label = e["label"]
                assigned_class = e["class"]
                assigned_color = e["color"]

        output_items.append({
            "label": assigned_label,
            "type": "AI",
            "color": assigned_color,
            "timestamp": t
        })

    return {"items": output_items}
