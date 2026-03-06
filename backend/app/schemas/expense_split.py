import uuid
from pydantic import BaseModel


class ExpenseSplitCreate(BaseModel):
    amount: float
    expense_id: uuid.UUID
    member_id: uuid.UUID


class ExpenseSplitUpdate(BaseModel):
    amount: float
    member_id: uuid.UUID


class ExpenseSplitResponse(BaseModel):
    id: uuid.UUID
    amount: float
    expense_id: uuid.UUID
    member_id: uuid.UUID

    class Config:
        from_attributes = True