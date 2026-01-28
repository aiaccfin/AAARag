# services/rag/ingestion.py
import uuid
from sqlmodel import Session
from app.models.rag.m_inv_vec import InvVecDB


class InvoiceIngestionService:
    def __init__(self, db: Session):
        self.db = db

    def ingest_invoice(
        self,        
        tenant_id: str,        
        invoice_id: uuid.UUID,        
        line_items: str,        
        notes: str,        
        summary: str,        
        content: str,
    ):
        obj = InvVecDB(
            tenant_id=tenant_id,
            invoice_id=invoice_id,
            line_items=line_items,
            notes=notes,
            summary=summary,
            content=content,
            line_items_embedding=None,
            notes_embedding=None,
            summary_embedding=None,
            content_embedding=None,
        )

        self.db.add(obj)
        try:
            self.db.commit()
        except:
            self.db.rollback()
            # Could use ON CONFLICT DO NOTHING or upsert logic
        self.db.refresh(obj)
        return obj
