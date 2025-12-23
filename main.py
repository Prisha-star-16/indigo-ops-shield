from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import pickle
from typing import Literal

# Initialize the "Attractive" API
app = FastAPI(
    title="IndiGo Ops Shield API",
    description="Predicts flight cancellation risks based on Crew FDTL & Weather parameters.",
    version="2.0",
    theme_color="#001B94" # Indigo color
)

# --- 1. Data Schema (The "Contract") ---
class FlightParams(BaseModel):
    origin_airport: str = Field(..., example="DEL", description="IATA code of origin")
    destination_airport: str = Field(..., example="BOM", description="IATA code of destination")
    pilots_required: int = Field(..., ge=2, example=2, description="Minimum crew required")
    pilots_available: int = Field(..., ge=0, example=1, description="Pilots currently available at hub")
    avg_duty_hours: float = Field(..., example=9.5, description="Average duty hours of assigned crew (FDTL metric)")
    aircraft_type: str = Field(..., example="A320", description="Aircraft model")
    
    class Config:
        schema_extra = {
            "example": {
                "origin_airport": "DEL",
                "destination_airport": "BLR",
                "pilots_required": 2,
                "pilots_available": 1,
                "avg_duty_hours": 10.2,
                "aircraft_type": "A321"
            }
        }

# --- 2. The Logic Layer (Replicating your Notebook) ---
def load_model():
    # In a real scenario, load your trained .pkl file here
    # model = pickle.load(open('indigo_cancellation_model.pkl', 'rb'))
    print("Loading AI Model...")
    return "DummyModel"

@app.post("/predict_risk", tags=["Operations"])
async def predict_cancellation(flight: FlightParams):
    """
    Analyzes flight parameters to predict cancellation probability.
    """
    # 1. Feature Engineering (As per your notebook)
    # New FDTL rules make pilot shortage a critical factor
    pilot_shortage = flight.pilots_required - flight.pilots_available
    
    # Peak duty flag: FDTL rules limit risk when duty > 9 hours
    peak_duty_flag = 1 if flight.avg_duty_hours > 9 else 0
    
    # 2. Heuristic / Model Logic (Simulating the Random Forest output)
    risk_score = 0.1 # Base risk
    
    if pilot_shortage > 0:
        risk_score += 0.60  # Massive risk spike if no pilots
    if peak_duty_flag == 1:
        risk_score += 0.25  # High risk due to fatigue rules
    
    # 3. Decision
    prediction = "CANCELLED" if risk_score > 0.5 else "ON_TIME"
    
    return {
        "flight_status_prediction": prediction,
        "risk_probability": f"{min(risk_score * 100, 99)}%",
        "critical_factors": {
            "pilot_shortage_severity": "HIGH" if pilot_shortage > 0 else "NONE",
            "fdtl_fatigue_warning": bool(peak_duty_flag)
        },
        "recommendation": "Urgent: Assign reserve crew or delay departure." if prediction == "CANCELLED" else "Operations Normal"
    }

# --- 3. Dashboard Endpoint ---
@app.get("/", tags=["General"])
def read_root():
    return {"message": "Welcome to IndiGo Ops Shield. Go to /docs for the interactive dashboard."}

# To run this: uvicorn main:app --reload