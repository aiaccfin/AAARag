from haystack.document_stores import PgvectorDocumentStore

document_store = PgvectorDocumentStore(
    connection_string="postgresql://postgres:postgrespwd@34.130.233.222:8000/xairls",
    embedding_dim=1536,          # matches EMBED_DIM
    table_name="invoice_embeddings",
    content_field="content",      # your invoice text
    embedding_field="embedding",  # pgvector column
)




# from haystack.document_stores.in_memory import InMemoryDocumentStore
# document_store = InMemoryDocumentStore()


# from datasets import load_dataset
# from haystack import Document

# dataset = load_dataset("bilgeyucel/seven-wonders", split="train")
# docs = [Document(content=doc["content"], meta=doc["meta"]) for doc in dataset]


# from haystack.components.embedders import SentenceTransformersDocumentEmbedder
# doc_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
# doc_embedder.warm_up()


# docs_with_embeddings = doc_embedder.run(docs)
# document_store.write_documents(docs_with_embeddings["documents"])

