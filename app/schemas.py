from pydantic import BaseModel, Field
from typing import Literal

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: Literal["admin", "faculty"]  # Restrict role choices

class UserResponse(BaseModel):
    id: int
    username: str
    role: Literal["admin", "faculty"]
    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    year: int = Field(..., gt=1999, lt=2100)  # Valid year range
    department: str
    faculty_count: int
    student_count: int
    lab_count: int
    building_area: float
    tuition_income: float
class ExpenseCreateWithCost(ExpenseCreate):
    total_cost: float

class ExpenseResponse(ExpenseCreate):
    id: int
    total_cost: float
    class Config:
        from_attributes = True

class TrackedExpenseCreate(BaseModel):
    year: int = Field(..., gt=1999, lt=2100)
    department: str
    faculty_expenses: float 
    training_expenses: float
    placement_expenses: float
    sports_expenses: float
    miscellaneous_expenses: float
    utilities: float
    rent: float

class TrackedExpenseResponse(TrackedExpenseCreate):
    id: int
    total_cost: float
    class Config:
        from_attributes = True

