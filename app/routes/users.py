from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserResponse
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


from app.routes.auth import get_password_hash
from faker import Faker
import random

fake = Faker()

@router.post("/setup-sample-users")
def setup_sample_users(db: Session = Depends(get_db)):
    # Optional: Check if users already exist
    if db.query(User).first():
        raise HTTPException(status_code=400, detail="Users already exist.")

    # Create admin
    admin = User(
        username="admin",
        password=get_password_hash("admin123"),
        role="admin"
    )
    db.add(admin)
    faculty=User(
        username="mohan",
        password=get_password_hash("chinu123"),
        role='faculty'
    )
    db.add(faculty)
    # Create 10 random faculty users
    for _ in range(10):
        username = fake.user_name()
        user = User(
            username=username,
            password=get_password_hash("password"),
            role="faculty"
        )
        db.add(user)

    db.commit()
    return {"message": "1 admin and 10 faculty users created successfully."}

