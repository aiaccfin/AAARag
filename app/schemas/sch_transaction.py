from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


# =========================
# Base
# =========================

class TransactionBase(BaseModel):
    tenant_id: UUID = "550e8400-e29b-41d4-a716-446655440000"

    amount: float
    currency: str = "USD"
    type: str = "transaction"
    from_account: str = "from"
    to_account: str = "to"

    memo: Optional[dict] = None
    reference: Optional[str] = None

    is_flagged: bool = False
    tags: Optional[List[str]] = None


# =========================
# Create
# =========================

class TransactionCreate(TransactionBase):
    pass


# =========================
# Update
# =========================

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    type: Optional[str] = None
    from_account: Optional[str] = None
    to_account: Optional[str] = None

    memo: Optional[dict] = None
    reference: Optional[str] = None

    is_flagged: Optional[bool] = None
    tags: Optional[List[str]] = None


# =========================
# Read
# =========================

class TransactionRead(TransactionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
