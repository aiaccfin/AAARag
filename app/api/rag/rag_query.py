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
    with langfuse.start_as_current_observation(
        as_type="span", name="rag-query"
    ) as span:
        # Embed query
        embedding_service = EmbeddingService()
        query_embedding = (await embedding_service.embed([payload.query]))[0]

        # Retrieve chunks
        retrieval_service = RetrievalService(db)
        results = retrieval_service.search(
            query_embedding=query_embedding, top_k=payload.top_k
        )

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
        with langfuse.start_as_current_observation(
            as_type="generation", name="llm-answer", model="gpt-4o"
        ) as generation:
            answer = generate_strict_answer(STRICT_PROMPT)
            generation.update(output=answer)

        # Update the main request span
        span.update(
            output=answer,
            metadata={
                "top_k": payload.top_k,
                "retrieved_chunk_ids": [c["chunk_id"] for c in results],
            },
        )

    # Flush events (good practice in short-lived apps)
    langfuse.flush()

    return {"answer": answer, "sources": results}


# @router.post("/haystack_query", response_model=QueryResponse)
# async def haystack_query_rag(
#     payload: QueryRequest,
#     db: Session = Depends(fun_get_session),
# ):
#     embedding_service = EmbeddingService()
#     retrieval_service = RetrievalService(db)

#     # ---- Haystack adapters ----
#     from haystack import Document, Pipeline
#     from haystack.components.generators import OpenAIGenerator
#     from haystack.components.retrievers import EmbeddingRetriever

#     class QueryEmbedder:
#         async def run(self, text: str):
#             embedding = (await embedding_service.embed([text]))[0]
#             return {"embedding": embedding}

#     class ExistingVectorStore:
#         def query_by_embedding(self, query_embedding, top_k: int):
#             results = retrieval_service.search(
#                 query_embedding=query_embedding,
#                 top_k=top_k
#             )
#             return [
#                 Document(
#                     content=r["content"],
#                     meta={
#                         "chunk_id": r["chunk_id"],
#                         "document_id": r["document_id"],
#                         "similarity": r["similarity"],
#                     },
#                 )
#                 for r in results
#             ]

#     embedder = QueryEmbedder()
#     document_store = ExistingVectorStore()

#     retriever = EmbeddingRetriever(
#         document_store=document_store,
#         top_k=payload.top_k
#     )

#     generator = OpenAIGenerator(
#         model="gpt-4o",
#         system_prompt="""You are a factual assistant.
# Rules:
# - Use ONLY the provided context
# - Cite facts with chunk IDs in brackets
# - If not found, reply exactly: "I don't know."
# """
#     )

#     def build_context(docs):
#         return "\n\n---\n\n".join(
#             f"[{d.meta['chunk_id']}] {d.content}" for d in docs
#         )

#     pipeline = Pipeline()
#     pipeline.add_component("embedder", embedder)
#     pipeline.add_component("retriever", retriever)
#     pipeline.add_component("generator", generator)

#     pipeline.connect("embedder.embedding", "retriever.query_embedding")
#     pipeline.connect("retriever.documents", "generator.documents")

#     result = await pipeline.run({
#         "embedder": {"text": payload.query},
#         "generator": {"prompt": payload.query},
#     })

#     answer = result["generator"]["replies"][0]
#     docs = result["retriever"]["documents"]

#     return {
#         "answer": answer,
#         "sources": [
#             {
#                 "chunk_id": d.meta["chunk_id"],
#                 "document_id": d.meta["document_id"],
#                 "content": d.content,
#                 "similarity": d.meta["similarity"],
#             }
#             for d in docs
#         ],
#     }


@router.post("/haystack_query", response_model=QueryResponse)
async def haystack_query_rag(
    payload: QueryRequest,
    db: Session = Depends(fun_get_session),
):
    from haystack import Document, Pipeline, component
    from haystack.components.builders import PromptBuilder
    from haystack.components.generators import OpenAIGenerator

    embedding_service = EmbeddingService()
    retrieval_service = RetrievalService(db)

    # compute embedding OUTSIDE haystack
    query_embedding = (await embedding_service.embed([payload.query]))[0]

    @component
    class ExistingDBRetriever:
        def __init__(self, top_k: int):
            self.top_k = top_k

        @component.output_types(documents=list[Document])
        def run(self, query_embedding: list[float]):
            results = retrieval_service.search(
                query_embedding=query_embedding, top_k=self.top_k
            )
            return {
                "documents": [
                    Document(
                        content=r["content"],
                        meta={
                            "chunk_id": r["chunk_id"],
                            "document_id": r["document_id"],
                            "similarity": r["similarity"],
                        },
                    )
                    for r in results
                ]
            }

    prompt_builder = PromptBuilder(
        template="""You are a factual assistant.
Rules:
- Use ONLY the information in the context
- Cite facts using chunk IDs in brackets
- If not found, reply exactly: "I don't know."

Context:
{% for doc in documents %}
[{{ doc.meta.chunk_id }}] {{ doc.content }}
{% endfor %}

Question:
{{ question }}

Answer:
"""
    )

    pipeline = Pipeline()
    pipeline.add_component("retriever", ExistingDBRetriever(payload.top_k))
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("generator", OpenAIGenerator(model="gpt-4o"))

    pipeline.connect("retriever.documents", "prompt_builder.documents")
    pipeline.connect("prompt_builder.prompt", "generator.prompt")

    result = pipeline.run(
        {
            "retriever": {"query_embedding": query_embedding},
            "prompt_builder": {"question": payload.query},
        },
        include_outputs_from=["retriever"],
    )

    answer = result["generator"]["replies"][0]
    docs = result["retriever"]["documents"]

    return {
        "answer": answer,
        "sources": [
            {
                "chunk_id": d.meta["chunk_id"],
                "document_id": d.meta["document_id"],
                "content": d.content,
                "similarity": d.meta["similarity"],
            }
            for d in docs
        ],
    }
