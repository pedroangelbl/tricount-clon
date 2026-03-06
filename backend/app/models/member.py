import uuid
from datetime import datetime

from app.db.database import Base
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Member(Base):
    __tablename__ = "members"

    # ========================
    # PRIMARY KEY
    # ========================
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # ========================
    # FIELDS
    # ========================
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="member")
    joined_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ========================
    # RELATIONSHIPS
    # ========================
    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="members")

    # gastos que ha pagado este miembro
    paid_expenses = relationship(
        "Expense", back_populates="paid_by", cascade="all, delete"
    )

    # divisiones de gastos donde participa
    expense_splits = relationship(
        "ExpenseSplit", back_populates="member", cascade="all, delete"
    )
