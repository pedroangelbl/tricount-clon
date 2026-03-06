import uuid
from datetime import datetime

from app.db.database import Base
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Group(Base):
    __tablename__ = "groups"

    # ========================
    # PRIMARY KEY
    # ========================
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # ========================
    # FIELDS
    # ========================
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ========================
    # RELATIONSHIPS
    # ========================
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    creator = relationship("User", back_populates="groups_created")
    members = relationship("Member", back_populates="group", cascade="all, delete")
    expenses = relationship("Expense", back_populates="group")
