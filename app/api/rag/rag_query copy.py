from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.services.rag.embeddings import EmbeddingService
from app.db.connection.conn_rls import get_super_session_factory
from app.services.rag.retrieval import RetrievalService
from app.llm.ai_api import generate_strict_answer
from langfuse import get_client

from dotenv import load_dotenv
load_dotenv()

fun_get_session = get_super_session_factory()
TENANT_ID = "550e8400-e29b-41d4-a716-446655440000"

router = APIRouter()

langfuse = get_client()

class ChunkResult(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    similarity: float

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: list[ChunkResult]

def build_context_with_source(chunks) -> str:
    return "\n\n---\n\n".join(f"[{c['chunk_id']}] {c['content']}" for c in chunks)


@router.post("/query", response_model=QueryResponse)
async def query_rag(
    payload: QueryRequest,
    db: Session = Depends(fun_get_session),
):
    # Start a Langfuse span for this request
    with langfuse.start_as_current_observation(as_type="span", name="rag-query") as span:
        # Embed query
        embedding_service = EmbeddingService()
        query_embedding = (await embedding_service.embed([payload.query]))[0]

        # Retrieve chunks
        retrieval_service = RetrievalService(db)
        results = retrieval_service.search(query_embedding=query_embedding, top_k=payload.top_k)

        # Build context with chunk IDs
        context = build_context_with_source(results)

        STRICT_PROMPT = f"""You are a factual assistant.
Rules:
- Use ONLY the information in the provided context.
- Cite each fact using the chunk IDs in brackets (e.g., [chunk_id]).
- If the answer cannot be found in the context, reply exactly with: "I don't know."
- Do NOT use prior knowledge.
- Do NOT speculate.

Context:
{context}

Question:
{payload.query}

Answer:
"""

        # Generate LLM answer inside a nested generation
        with langfuse.start_as_current_observation(as_type="generation", name="llm-answer", model="gpt-4o") as generation:
            answer = generate_strict_answer(STRICT_PROMPT)
            generation.update(output=answer)

        # Update the main request span
        span.update(
            output=answer,
            metadata={
                "top_k": payload.top_k,
                "retrieved_chunk_ids": [c["chunk_id"] for c in results]
            }
        )

    # Flush events (good practice in short-lived apps)
    langfuse.flush()

    return {
        "answer": answer,
        "sources": results
    }




# from typing import List
# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
# from sqlmodel import Session
# from app.services.rag.ingestion import IngestionService
# from app.services.rag.embeddings import EmbeddingService
# from app.helpers.tenant_id import get_tenant_id
# from app.db.connection.conn_rls import get_super_session_factory
# from app.services.rag.retrieval import RetrievalService
# from app.llm.ai_api import generate_strict_answer

# from app.llm.langfuse_client import lf_client

# fun_get_session = get_super_session_factory()

# router = APIRouter()
# TENANT_ID = "550e8400-e29b-41d4-a716-446655440000"


# class QueryRequest(BaseModel):
#     query: str
#     top_k: int = 5

# class ChunkResult(BaseModel):
#     chunk_id: str
#     document_id: str
#     content: str
#     similarity: float

# class QueryResponse(BaseModel):
#     results: List[ChunkResult]


# class RAGResponse(BaseModel):
#     answer: str
#     sources: List[ChunkResult]


# def build_context(chunks, max_chars=3000) -> str:
#     context_parts = []
#     total = 0

#     for c in chunks:
#         text = c["content"]
#         if total + len(text) > max_chars:
#             break
#         context_parts.append(text)
#         total += len(text)

#     return "\n\n---\n\n".join(context_parts)


# @router.post("/query", response_model=RAGResponse)
# async def query_rag(
#     payload: QueryRequest,
#     db: Session = Depends(fun_get_session),
# ):
#     embedding_service = EmbeddingService()
#     query_embedding = (await embedding_service.embed([payload.query]))[0]

#     retrieval_service = RetrievalService(db)
#     results = retrieval_service.search(query_embedding=query_embedding, top_k=payload.top_k)

#     context = build_context(results)

#     STRICT_PROMPT = """You are a factual assistant.
#         Rules:
#         - Use ONLY the information in the provided context.
#         - If the answer cannot be found in the context, reply exactly with: "I don't know."
#         - Do NOT use prior knowledge.
#         - Do NOT speculate.

#         Context:
#         {context}

#         Question:
#         {question}

#         Answer:
#         """

#     prompt = STRICT_PROMPT.format(
#         context=context,
#         question=payload.query
#     )

#     answer = generate_strict_answer(prompt)
    
#     # Log the RAG query
#     lf_client.track(
#         model_name="gpt-4o",
#         input=payload.query,
#         output=answer,
#         metadata={
#             "tenant_id": TENANT_ID,
#             "top_k": payload.top_k,
#             "retrieved_chunk_ids": [c["chunk_id"] for c in results]
#         }
#     )
        
#     return {
#         "answer": answer,
#         "sources": results
#     }