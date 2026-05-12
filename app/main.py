# run command: uvicorn app.main:app --reload

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from uuid import UUID
import hashlib
from datetime import datetime, timezone


from app.db import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserResponse
from typing import List

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.execute(select(User).where(User.deleted_at.is_(None))).scalars().all()
    return users


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # validar duplicado
    existing_user = db.execute(select(User).where(User.email == user.email)).scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # hash the plain text password
    hashed_pwd = hashlib.sha256(user.password.encode('utf-8')).hexdigest()

    db_user = User(
        email=user.email,
        password_hash=hashed_pwd,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database Integrity Error: {str(e.orig)}")

    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.deleted_at = datetime.now(timezone.utc)
    db.commit()

    return {"message": "User deleted"}