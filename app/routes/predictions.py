import pickle
import os
from fastapi import APIRouter, HTTPException, Depends
from .auth import require_role
from app.schemas import ExpenseCreate
from app.utils import load_model, load_encoder
import pandas as pd


router = APIRouter()

# Load trained model and label encoder
model = load_model()
le = load_encoder()

model = load_model()
le = load_encoder()

if model is None:
    raise HTTPException(status_code=500, detail="Failed to load the prediction model.")
if le is None:
    raise HTTPException(status_code=500, detail="Failed to load the label encoder.")


@router.post("/", dependencies=[Depends(require_role("admin"))])
def predict_cost(expense: ExpenseCreate):
    try:
        department_encoded = le.transform([expense.department])[0]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid department value: {expense.department}")

    try:
        # Construct input data according to trained model's expected features
        input_data = {
            "Year": expense.year,
            "Department": department_encoded,
            "Faculty_Count": expense.faculty_count,
            "Student_Count": expense.student_count,
            "Lab_Count": expense.lab_count,
            "Building_Area": expense.building_area,
            "Tuition_Income": expense.tuition_income,
        }

        # Convert to DataFrame and predict
        input_df = pd.DataFrame([input_data])
        prediction = round(model.predict(input_df)[0], 2)
        print(prediction)

        return {"predicted_total_cost": prediction}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
