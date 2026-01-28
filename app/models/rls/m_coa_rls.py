from typing import Optional, Dict, Any, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey

import uuid
from datetime import datetime

# contains tenant_id, id, created_at, etc.
from app.models.m_mixin import BaseMixin

if TYPE_CHECKING:
    from app.models.rls.m_coa_rls import COADB


class COABase(SQLModel):
    """
    Master chart of COAs with nested (hierarchical) support.
    """
    code: str = Field(index=True, description="Unique COA code")
    name: str = Field(description="COA name")
    type: str = Field(description="Asset, Liability, Equity, Revenue, Expense")
    currency: Optional[str] = Field(default=None)

    # Optional metadata
    extras: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSONB))


class COADB(BaseMixin, COABase,  table=True):
    __tablename__ = "coa_rls"

    # Self-referential hierarchy - using sa_column with ForeignKey for RLS tables
    parent_id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(ForeignKey("coa_rls.id", ondelete="SET NULL"), nullable=True, index=True)
    )

    # ORM relationships for hierarchical navigation
    # For self-referential relationships, we need to set remote_side properly
    children: List["COADB"] = Relationship(back_populates="parent")
    parent: Optional["COADB"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={
            "primaryjoin": "COADB.parent_id == COADB.id",
            "remote_side": "COADB.id"
        }
    )


class COACreate(COABase):
    parent_id: Optional[uuid.UUID] = None


class COARead(COABase):
    id: uuid.UUID
    parent_id: Optional[uuid.UUID] = None
