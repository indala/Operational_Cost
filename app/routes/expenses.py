from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import String, asc, desc
from app.database import get_db
from .auth import get_current_user, require_role
from app import models, schemas
import csv
from io import StringIO
from sqlalchemy.sql import cast, func, or_

router = APIRouter()

# ✅ Create a single tracked expense (manual form submission)
@router.post("/", dependencies=[Depends(require_role("admin"))])
def create_expense(expense: schemas.TrackedExpenseCreate, db: Session = Depends(get_db)):
    total_cost = (
        expense.training_expenses + 
        expense.placement_expenses + 
        expense.sports_expenses + 
        expense.miscellaneous_expenses + 
        expense.utilities + 
        expense.rent + 
        expense.faculty_expenses  # Include faculty_expenses in total cost calculation
    )

    db_expense = models.TrackedExpense(**expense.model_dump(exclude_unset=True), total_cost=total_cost)

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


# ✅ Get all tracked expenses with pagination, search, and sorting
@router.get("/", dependencies=[Depends(get_current_user)])
def get_expenses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    search: str = Query("", alias="search"),
    sort_by: str = Query("year", alias="sort_by"),
    order: str = Query("asc", alias="order")
):
    query = db.query(models.TrackedExpense)

    if search:
        query = query.filter(
            or_(
                func.lower(models.TrackedExpense.department).like(f"%{search.lower()}%"),
                cast(models.TrackedExpense.year, String).like(f"%{search}%")
            )
        )

    sort_column = getattr(models.TrackedExpense, sort_by, None)
    if sort_column is not None:
        sort_order = desc(sort_column) if order == "desc" else asc(sort_column)
        query = query.order_by(sort_order)

    total_count = query.count()
    expenses = query.offset(skip).limit(limit).all()

    return {"total_count": total_count, "expenses": expenses}


# ✅ Bulk upload via CSV (admin-only)
@router.post("/upload_csv", dependencies=[Depends(require_role("admin"))])
async def upload_expenses_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    csv_data = contents.decode("utf-8")
    reader = csv.DictReader(StringIO(csv_data))

    created_expenses = []
    failed_rows = []

    for row in reader:
        try:
            expense = schemas.TrackedExpenseCreate(
                year=int(row["Year"]),
                department=row["Department"],
                training_expenses=float(row["Training_Expenses"]),
                placement_expenses=float(row["Placement_Expenses"]),
                sports_expenses=float(row["Sports_Expenses"]),
                miscellaneous_expenses=float(row["Miscellaneous_Expenses"]),
                utilities=float(row["Utilities"]),
                rent=float(row["Rent"]),
                faculty_expenses=float(row["Faculty_Expenses"]),  # 🆕 Added field
                total_cost=float(row["Total_Cost"])
            )

            db_expense = models.TrackedExpense(**expense.model_dump())
            db.add(db_expense)
            created_expenses.append(db_expense)

        except Exception as e:
            failed_rows.append({"row": row, "error": str(e)})

    db.commit()

    if failed_rows:
        return {
            "message": f"{len(created_expenses)} expenses uploaded successfully.",
            "failed_rows": failed_rows
        }

    return {"message": f"{len(created_expenses)} expenses uploaded successfully"}

@router.post("/save_prediction", dependencies=[Depends(require_role("admin"))])
def save_predicted_expense(expense: schemas.ExpenseCreateWithCost, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


