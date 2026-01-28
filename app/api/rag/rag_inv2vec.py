import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.connection.conn_rls import get_super_session_factory
from app.services.rag.service_inv2vec import InvoiceIngestionService
from app.models.rag.m_inv_vec import InvoiceIngestRequest, InvoiceEmbedRequest

router = APIRouter()
TENANT_ID = "550e8400-e29b-41d4-a716-446655440000"

fun_get_session = get_super_session_factory()


# -------------------------
# Ingest Invoice Endpoint
# -------------------------
@router.post("/inv2vec")
async def ingest_invoice(
    payload: InvoiceIngestRequest,
    db: Session = Depends(fun_get_session),
    tenant_id: str = TENANT_ID
):
    """
    Ingests invoice text into invoice_vectors table.
    Only stores textual content, embeddings are left null.
    """
    service = InvoiceIngestionService(db=db)
    invoice = service.ingest_invoice(
        tenant_id=tenant_id,
        invoice_id=payload.invoice_id,
        line_items=payload.line_items,
        notes=payload.notes,
        summary=payload.summary,
        content=payload.content
    )

    return {"invoice_id": invoice.invoice_id}


# # -------------------------
# # Embed Invoice Endpoint
# # -------------------------
# @router.post("/vec2embed")
# async def embed_invoice(
#     payload: InvoiceEmbedRequest,
#     db: Session = Depends(fun_get_session),
#     tenant_id: str = TENANT_ID
# ):
#     """
#     Generates embeddings for specified columns of an invoice.
#     If `columns` is None, embeds all textual columns.
#     """
#     embed_service = EmbeddingService()
#     service = InvoiceEmbeddingService(db=db, embed_model=embed_service)

#     invoice = service.embed_invoice(
#         invoice_id=payload.invoice_id,
#         columns=payload.columns  # Optional list: ['line_items','notes','summary','content']
#     )

#     return {
#         "invoice_id": invoice.invoice_id,
#         "embeddings_done": True,
#         "embedded_columns": payload.columns or ["line_items","notes","summary","content"]
#     }
