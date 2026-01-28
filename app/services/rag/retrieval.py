# services/rag/retrieval.py
from sqlmodel import Session, text
from typing import List, Dict

class RetrievalService:
    def __init__(self, db: Session):
        self.db = db

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        embedding_str = "ARRAY[" + ",".join(map(str, query_embedding)) + "]::vector"
        sql = text(f"""
        SELECT id, document_id, content, embedding <-> {embedding_str} AS similarity
        FROM documentchunk
        ORDER BY embedding <-> {embedding_str}
        LIMIT :top_k
        """)
        result = self.db.execute(sql, {"top_k": top_k}).all()
        return [
            {
                "chunk_id": str(row.id),
                "document_id": str(row.document_id),
                "content": row.content,
                "similarity": float(row.similarity)
            }
            for row in result
        ]
