import uuid

from app.db.database import Base
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    # ========================
    # PRIMARY KEY
    # ========================
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # ========================
    # FIELDS
    # ========================
    amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)

    # ========================
    # RELATIONSHIPS
    # ========================
    expense_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("expenses.id", ondelete="cascade"), nullable=False
    )
    member_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("members.id", ondelete="cascade"), nullable=False
    )

    expense = relationship("Expense", back_populates="splits")
    member = relationship("Member", back_populates="expense_splits")
