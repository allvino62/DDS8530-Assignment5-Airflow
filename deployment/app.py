from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    BASE_DIR / "models" / "sales_prediction_model.pkl"
)

model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="DDS8530 Customer Sales Prediction API",
    description="Random Forest Model Deployment",
    version="1.0"
)


class SalesInput(BaseModel):
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    discount: float = Field(ge=0, le=1)


@app.get("/")
def home():
    return {
        "project": "DDS8530 Assignment 5",
        "model": "Customer Sales Random Forest",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": True
    }


@app.post("/predict")
def predict_sales(data: SalesInput):

    input_data = pd.DataFrame([{
        "quantity": data.quantity,
        "unit_price": data.unit_price,
        "discount": data.discount
    }])

    prediction = model.predict(input_data)[0]

    return {
        "quantity": data.quantity,
        "unit_price": data.unit_price,
        "discount": data.discount,
        "predicted_total_sales": round(
            float(prediction), 2
        ),
        "model": "RandomForestRegressor"
    }
# Prometheus monitoring integration
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
