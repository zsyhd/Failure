from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

class AIItem(BaseModel):
    label: str
    timestamp: str

class PredictionRequest(BaseModel):
    ai_items: List[AIItem]

@app.get("/")
def read_root():
    return {"message": "Failure Prediction API is running. Use /predict (POST) to get predictions."}

@app.post("/predict")
def predict_failure(data: PredictionRequest):
    result = {
        "total_items": len(data.ai_items),
        "labels": [item.label for item in data.ai_items]
    }
    return result
