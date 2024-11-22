from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from src.models.p2p_loan import LoanRequest, User
from src.database import get_db
from src.auth import get_current_user

router = APIRouter()

class LoanRequestCreate(BaseModel):
    amount: float
    interest_rate: float
    duration_months: int

class LoanRequestUpdate(BaseModel):
    amount: float = None
    interest_rate: float = None
    duration_months: int = None

@router.post("/loans/", response_model=LoanRequest)
def create_loan_request(loan_request: LoanRequestCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_loan_request = LoanRequest(
        id=str(uuid.uuid4()),
        borrower_id=current_user.id,
        amount=loan_request.amount,
        interest_rate=loan_request.interest_rate,
        duration_months=loan_request.duration_months
    )
    db.add(new_loan_request)
    db.commit()
    db.refresh(new_loan _request)
    return new_loan_request

@router.get("/loans/", response_model=List[LoanRequest])
def get_loan_requests(db: Session = Depends(get_db)):
    return db.query(LoanRequest).all()

@router.get("/loans/{loan_id}", response_model=LoanRequest)
def get_loan_request(loan_id: str, db: Session = Depends(get_db)):
    loan_request = db.query(LoanRequest).filter(LoanRequest.id == loan_id).first()
    if not loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found")
    return loan_request

@router.put("/loans/{loan_id}", response_model=LoanRequest)
def update_loan_request(loan_id: str, loan_request: LoanRequestUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_loan_request = db.query(LoanRequest).filter(LoanRequest.id == loan_id, LoanRequest.borrower_id == current_user.id).first()
    if not db_loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found or not authorized")
    
    if loan_request.amount is not None:
        db_loan_request.amount = loan_request.amount
    if loan_request.interest_rate is not None:
        db_loan_request.interest_rate = loan_request.interest_rate
    if loan_request.duration_months is not None:
        db_loan_request.duration_months = loan_request.duration_months

    db.commit()
    db.refresh(db_loan_request)
    return db_loan_request

@router.delete("/loans/{loan_id}", response_model=dict)
def delete_loan_request(loan_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_loan_request = db.query(LoanRequest).filter(LoanRequest.id == loan_id, LoanRequest.borrower_id == current_user.id).first()
    if not db_loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found or not authorized")
    
    db.delete(db_loan_request)
    db.commit()
    return {"detail": "Loan request deleted successfully"}
