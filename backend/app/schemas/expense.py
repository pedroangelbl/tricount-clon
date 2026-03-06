import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.expense_split import ExpenseSplitCreate


class ExpenseCreate(BaseModel):
    title: str
    amount: float
    currency: str = "EUR"
    description: str | None = None
    group_id: uuid.UUID
    splits: List[ExpenseSplitCreate]


class ExpenseUpdate(BaseModel):
    title: str
    amount: float
    currency: str = "EUR"
    description: str | None = None


class ExpenseResponse(BaseModel):
    id: uuid.UUID
    title: str
    amount: float
    currency: str = "EUR"
    description: str | None = None
    expense_date: datetime
    created_at: datetime
    group_id: uuid.UUID
    paid_by_member_id: uuid.UUID

    class Config:
        from_attributes = True
