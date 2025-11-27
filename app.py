from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

class AIItem(BaseModel):
    label: str
    timestamp: str

class AIData(BaseModel):
    ai_items: List[AIItem]

@app.get("/")
def read_root():
    return {"message": "Failure Prediction API is running. Use /predict (POST) to get predictions."}

@app.post("/predict")
async def predict(data: AIData):
    predictions = []
    for item in data.ai_items:
        predictions.append({
            "label": item.label,
            "timestamp": item.timestamp,
            "predicted_failure": "yes" if item.label != "normal" else "no"
        })

    return {"predictions": predictions}
