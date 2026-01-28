import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.services.rag.ingestion import IngestionService
from app.services.rag.embeddings import EmbeddingService
from app.helpers.tenant_id import get_tenant_id
from app.db.connection.conn_rls import get_super_session_factory

fun_get_session = get_super_session_factory()

router = APIRouter()
TENANT_ID = "550e8400-e29b-41d4-a716-446655440000"

class DocumentIngestRequest(BaseModel):
    source: str
    content: str

class DocumentIngestResponse(BaseModel):
    document_id: uuid.UUID
    chunks: int


# implemented a full ingestion pipeline that chunks documents, generates embeddings asynchronously, and stores them in Postgres using pgvector with proper transaction handling.
@router.post("/ingest", response_model=DocumentIngestResponse)
async def ingest_document(
    payload: DocumentIngestRequest,
    db: Session = Depends(fun_get_session),
    tenant_id=TENANT_ID,
):
    service = IngestionService(
        db=db,
        embedding_service=EmbeddingService()
    )
    
    print('---------', IngestionService.ingest.__code__.co_varnames)

    result = await service.ingest(
        tenant_id=tenant_id,
        source=payload.source,
        content=payload.content
    )
    return result




# Models: Document + DocumentChunk
# Chunking: configurable, overlap supported
# Embedding: async, pluggable
# Ingestion service: handles full flow
# API router: thin layer, calls service only




# POST /rag/query
#   └─> Query text
#       └─> EmbeddingService.embed() → query vector
#       └─> Vector search in DB → candidate chunks
#       └─> Optional reranking / metadata filtering
#       └─> Assemble context for LLM
#       └─> Return top-K chunks
