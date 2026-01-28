from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from haystack import Document
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from app.db.connection.conn_rls import get_super_session_factory
from app.models.rls.m_invoice_rls import InvoiceDB  # your invoice model

router = APIRouter()
fun_get_session = get_super_session_factory()

from pydantic import BaseModel

class InvoiceCloneRequest(BaseModel):
    limit: int | None = 100

@router.post("/haystack_inv_clone")
def clone_invoices_to_document_store(
    payload: InvoiceCloneRequest,
    db: Session = Depends(fun_get_session),
):
    # 1. Fetch invoices
    stmt = select(InvoiceDB)

    if payload.limit:
        stmt = stmt.limit(payload.limit)

    invoices = db.exec(stmt).all()

    if not invoices:
        return {"inserted": 0}

    # 2. Init Haystack Pgvector store
    document_store = PgvectorDocumentStore(
        embedding_dimension=1536,
        table_name="invoice_embeddings",
    )

    # 3. Convert invoices → Documents
    documents: list[Document] = []

    for inv in invoices:
        customer = inv.customer_snapshot or {}
        content = (
            f"Invoice {inv.invoice_number}\n"
            f"Customer: {customer.get('customer_name', 'N/A')}\n"
            f"Total: {inv.total_amount}\n"
            f"Issue date: {inv.issue_date}\n"
            f"Due date: {inv.due_date}\n"
            f"Description: {inv.description}\n"
        )

        doc = Document(
            content=content,
            meta={
                "invoice_id": str(inv.id),
                "total": inv.total_amount,
                "issue_date": inv.issue_date.isoformat(),
            },
        )
        documents.append(doc)

    # 4. Write to Haystack store
    document_store.write_documents(documents)

    return {
        "inserted": len(documents),
    }
