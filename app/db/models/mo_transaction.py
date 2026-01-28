import uuid
from datetime import datetime
from sqlalchemy import String, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.models.mo_base import Base, BaseMixin

class Transaction(Base, BaseMixin):
    __tablename__ = "transactions"

    # Core transaction data
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="transaction")  # transaction / transfer
    from_account: Mapped[str] = mapped_column(String(50), nullable=False, default="from")  # transaction / transfer
    to_account: Mapped[str] = mapped_column(String(50), nullable=False, default="to")  # transaction / transfer

    # User-entered flexible data
    memo: Mapped[dict] = mapped_column(JSONB, nullable=True)  # store arbitrary JSON


    # Optional reference / notes
    reference: Mapped[str] = mapped_column(String(50), nullable=True)

    # Extra fields for convenience
    is_flagged: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[list] = mapped_column(JSONB, nullable=True)  # e.g., ["salary", "bonus"]

