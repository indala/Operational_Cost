from sqlalchemy import Column, Integer, String, Float
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # "admin" or "faculty"

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    department = Column(String, index=True)
    faculty_count = Column(Integer)
    student_count = Column(Integer)
    lab_count = Column(Integer)
    building_area = Column(Float)
    tuition_income = Column(Float)
    total_cost = Column(Float)

# ✅ Modified: Added faculty_expenses field
class TrackedExpense(Base):
    __tablename__ = "tracked_expenses"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    department = Column(String)
    faculty_expenses = Column(Float)  # 🆕 New field
    training_expenses = Column(Float)
    placement_expenses = Column(Float)
    sports_expenses = Column(Float)
    miscellaneous_expenses = Column(Float)
    utilities = Column(Float)
    rent = Column(Float)
    total_cost = Column(Float)
