from typing import Optional, Dict, Any, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey
from pgvector.sqlalchemy import Vector
import uuid
from datetime import datetime
from app.models.m_mixin import BaseMixin

class Document(BaseMixin, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DocumentChunk(BaseMixin, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="document.id")
    chunk_index: int
    content: str

    embedding: Optional[list[float]] = Field(
        sa_column=Column(Vector(1536))
    )


# CREATE INDEX document_chunk_embedding_idx
# ON documentchunk
# USING ivfflat (embedding vector_cosine_ops)
# WITH (lists = 100);

# SELECT  id,  vector_dims(embedding)FROM documentchunk ;
