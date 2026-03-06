import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit


router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("", response_model=list[ExpenseResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(Expense).all()
    
@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: uuid.UUID, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.post("", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        currency=expense.currency,
        description=expense.description,
        group_id=expense.group_id,
    )

    db.add(db_expense)
    db.flush() # para obtener el id antes de hacer los splits
    
    splits = []
    for split in expense.splits:
        expense_split = ExpenseSplit(
            amount=split.amount,
            expense_id=db_expense.id,
            member_id=split.member_id
        )
        db.add(expense_split)
        splits.append(expense_split)
    
    db.commit()
    db.refresh(db_expense)

    db_expense.splits = splits

    return db_expense
    