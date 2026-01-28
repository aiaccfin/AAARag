from fastapi import APIRouter, Depends

# from app.api.v7 import endpoint_invoice
from app.utils.u_auth_py import authent
from app.api.rag import rag_ingest
from app.api.rag import rag_inv2vec
from app.api.rag import rag_query

ragRou = APIRouter()

# v7Router.include_router(endpoint_invoice.router, prefix="/invoice", tags=["v7_invoice"], dependencies=[Depends(authent)])
ragRou.include_router(rag_ingest.router, prefix="/rag", tags=["Global RAG"], dependencies=[Depends(authent)])
ragRou.include_router(rag_query.router, prefix="/rag", tags=["Global RAG"], dependencies=[Depends(authent)])
ragRou.include_router(rag_inv2vec.router, prefix="/rag", tags=["Global RAG"], dependencies=[Depends(authent)])