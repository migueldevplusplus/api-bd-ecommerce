from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from datetime import datetime


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
    users = db.query(User).filter(User.deleted_at == None).all()
    return users


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # validar duplicado
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        email=user.email,
        password_hash=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.deleted_at = datetime.utcnow()
    db.commit()

    return {"message": "User deleted"}