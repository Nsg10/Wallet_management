import os
from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI, Depends, status, HTTPException, Path
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User, Wallet, Transaction
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime



# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class WalletUpdate(BaseModel):
    amount: float

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    wallet_balance: Optional[float] = 0.0

    class Config:
        orm_mode = True

class TransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    timestamp: datetime

    class Config:
        orm_mode = True

@app.get("/")
def root():
    return {"message": "Wallet API is running."}

@app.get("/users", response_model=List[UserOut], status_code=status.HTTP_200_OK)
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    result = []
    for user in users:
        wallet_balance = user.wallet.balance if user.wallet else 0.0
        result.append(
            UserOut(
                id=user.id,
                name=user.name,
                email=user.email,
                phone=user.phone,
                wallet_balance=wallet_balance,
            )
        )
    return result

@app.get("/transactions/{user_id}", response_model=List[TransactionOut], status_code=status.HTTP_200_OK)
def fetch_transactions(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )
    return transactions

@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.phone == user.phone)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or phone already registered")

    new_user = User(name=user.name, email=user.email, phone=user.phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserOut(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        phone=new_user.phone,
        wallet_balance=0.0,
    )

@app.post("/wallet/{user_id}", status_code=status.HTTP_200_OK)
def update_wallet(
    update: WalletUpdate,
    user_id: int = Path(..., description="ID of the user"),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()

    if wallet:
        wallet.balance += update.amount
    else:
        wallet = Wallet(user_id=user_id, balance=update.amount)
        db.add(wallet)

    transaction = Transaction(user_id=user_id, amount=update.amount)
    db.add(transaction)

    db.commit()
    db.refresh(wallet)

    return {"user_id": user_id, "updated_balance": wallet.balance}
