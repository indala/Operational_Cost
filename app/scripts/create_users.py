import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import random
from faker import Faker
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import SessionLocal, engine
from app.models import User, Base

# Initialize database and Faker
Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()
fake = Faker()

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def create_admin():
    admin = User(
        username="admin",
        password=hash_password("admin123"),
        role="admin"
    )
    db.add(admin)

def create_random_users(n=10):
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            password=hash_password("password123"),
            role="faculty"
        )
        db.add(user)

def main():
    create_admin()
    create_random_users(10)
    db.commit()
    print("✅ Admin and random users created successfully!")

if __name__ == "__main__":
    main()
