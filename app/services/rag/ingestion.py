# services/rag/ingestion.py
import uuid
from sqlmodel import Session
from app.models.rag.m_document import Document, DocumentChunk
from app.services.rag.chunking import chunk_text
from app.services.rag.embeddings import EmbeddingService

class IngestionService:
    def __init__(self, db: Session, embedding_service: EmbeddingService):
        self.db = db
        self.embedding_service = embedding_service

    async def ingest(self, tenant_id: uuid.UUID, source: str, content: str) -> dict:
        # 1️⃣ Create document
        document = Document(tenant_id=tenant_id, source=source)
        self.db.add(document)
        self.db.flush()  # get document.id without commit

        # 2️⃣ Chunk
        chunks = chunk_text(content)

        # 3️⃣ Embed all chunks in batch
        embeddings = await self.embedding_service.embed(chunks)

        # 4️⃣ Create chunk rows
        chunk_rows = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_rows.append(
                DocumentChunk(
                    document_id=document.id,
                    tenant_id=document.tenant_id,
                    chunk_index=idx,
                    content=chunk,
                    embedding=embedding
                )
            )

        self.db.add_all(chunk_rows)
        self.db.commit()

        return {
            "document_id": document.id,
            "chunks": len(chunk_rows)
        }
