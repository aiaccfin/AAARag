from typing import Optional, List
from sqlmodel import SQLModel, Field, Column
from pgvector.sqlalchemy import Vector
import uuid
from datetime import datetime
from app.models.m_mixin import BaseMixin

EMBED_DIM = 1536  # adjust to your embedding model

class InvVecDB(BaseMixin, table=True):
    __tablename__ = "invoice_vectors"

    invoice_id: uuid.UUID

    # Multi-column text fields
    line_items: Optional[str] = None
    notes: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None  # optional full-text fallback

    # Corresponding embeddings
    line_items_embedding: Optional[List[float]] = Field(
        sa_column=Column(Vector(EMBED_DIM), nullable=True)
    )
    notes_embedding: Optional[List[float]] = Field(
        sa_column=Column(Vector(EMBED_DIM), nullable=True)
    )
    summary_embedding: Optional[List[float]] = Field(
        sa_column=Column(Vector(EMBED_DIM), nullable=True)
    )
    content_embedding: Optional[List[float]] = Field(
        sa_column=Column(Vector(EMBED_DIM), nullable=True)
    )

    # Optional chunking metadata
    chunk_index: int = Field(default=1)
    chunk_type: Optional[str] = Field(default="line_item")


import uuid
from typing import Optional
from pydantic import BaseModel, Field


# --------------------------
# Request model for ingestion
# --------------------------
class InvoiceIngestRequest(BaseModel):
    invoice_id: uuid.UUID = Field(..., description="Unique invoice ID")
    line_items: Optional[str] = Field(None, description="Text representation of line items")
    notes: Optional[str] = Field(None, description="Invoice notes or comments")
    summary: Optional[str] = Field(None, description="Short summary of invoice")
    content: Optional[str] = Field(None, description="Optional full text / fallback content")

    class Config:
        json_schema_extra = {
            "example": {
                "invoice_id": "550e8400-e29b-41d4-a716-446655440000",
                "line_items": "1x Consulting Service - $500, 2x AWS Hosting - $300",
                "notes": "Client requested early delivery",
                "summary": "Invoice total $800 for consulting and hosting",
                "content": "Full invoice text if needed for fallback search"
            }
        }


# --------------------------
# Request model for embedding
# --------------------------
class InvoiceEmbedRequest(BaseModel):
    invoice_id: uuid.UUID = Field(..., description="Invoice ID to generate embeddings for")
    columns: Optional[list[str]] = Field(
        None,
        description=(
            "Optional list of columns to embed. "
            "Defaults to all text columns if not provided. "
            "Valid options: ['line_items', 'notes', 'summary', 'content']"
        ),
    )

    class Config:
        json_schema_extra = {
            "example": {
                "invoice_id": "550e8400-e29b-41d4-a716-446655440000",
                "columns": ["line_items", "notes"]
            }
        }
