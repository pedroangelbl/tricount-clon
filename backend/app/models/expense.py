import uuid
from datetime import datetime

from app.db.database import Base
from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Expense(Base):
    __tablename__ = "expenses"

    # ========================
    # PRIMARY KEY
    # ========================
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # ========================
    # FIELDS
    # ========================
    title: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False, default="EUR")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    expense_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ========================
    # RELATIONSHIPS
    # ========================
    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id"), nullable=False
    )
    paid_by_member: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("members.id"), nullable=False
    )

    group = relationship("Group", back_populates="expenses")
    paid_by = relationship("Member", back_populates="paid_expenses")
    splits = relationship(
        "ExpenseSplit", back_populates="expense", cascade="all, delete"
    )
