from typing import List, Dict, Any
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from services.embeddings import get_embedding_model
from config import settings

def retrieve_relevant_chunks(question: str, institution_id: str, top_k: int = 4) -> List[Dict[str, Any]]:
    """
    Queries ChromaDB for policy document chunks relevant to the user query.
    Data isolation is strictly enforced by querying the tenant-specific collection.
    """
    chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    
    # Using tenant-specific collection for strict data isolation
    chroma_collection = chroma_client.get_or_create_collection(f"policy_documents_{institution_id}")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    embed_model = get_embedding_model()
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model
    )

    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(question)

    results = []
    for node in nodes:
        results.append({
            "text": node.node.get_content(),
            "filename": node.node.metadata.get("filename", "Unknown"),
            "page_number": node.node.metadata.get("page_number", 0),
            "score": float(node.score) if node.score else 0.0
        })

    return results