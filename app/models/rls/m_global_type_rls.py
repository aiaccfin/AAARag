# app/models/type.py
from typing import ClassVar, Optional, Dict, Any, List, Sequence

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID

from datetime import datetime
from typing import Optional
import uuid


class TypeBase(SQLModel):
    category: str = Field(index=True, default="customer type")         # e.g. "payment", "invoice_status"
    label: str = Field(default="customer")
    value: Optional[str] = Field(default="5 star customer")                # Optional machine value
    sort_order: int = 0                        # For dropdown ordering
    is_active: bool = True                     # Soft-disable
    notes: Dict[str, Any] = Field(
        default={}, sa_column=Column(JSONB))  
    description: Optional[str] = Field(default=None)  # Optional description


class TypeDB(TypeBase, table=True):
    __tablename__ = "global_types"
    __table_args__ = (
        UniqueConstraint("tenant_id", "category", "value", name="uix_tenant_category_value"),
    )
    tenant_id: uuid.UUID = Field(index=True)  # RLS / multi-tenant
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = Field(default="aiagent")
    updated_by: Optional[str] = Field(default="mcp")
    
    
class TypeCreate(TypeBase):
    pass


class TypeRead(TypeBase):
    id: uuid.UUID  # 🔥 改为 UUID

