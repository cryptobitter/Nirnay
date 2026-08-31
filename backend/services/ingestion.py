import io
import chromadb
from pypdf import PdfReader
from llama_index.core import Document as LlamaDocument
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from services.embeddings import get_embedding_model
from config import settings

def process_and_index_pdf(file_bytes: bytes, filename: str, institution_id: str) -> int:
    """
    Parses PDF bytes, splits text into chunks, attaches institution metadata,
    embeds the content, and persists it into Chroma vector store.
    Returns page count.
    """
    pdf_reader = PdfReader(io.BytesIO(file_bytes))
    page_count = len(pdf_reader.pages)

    llama_docs = []
    for index, page in enumerate(pdf_reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            llama_docs.append(
                LlamaDocument(
                    text=text,
                    extra_info={
                        "filename": filename,
                        "page_number": index + 1,
                        "institution_id": str(institution_id)
                    }
                )
            )

    if not llama_docs:
        raise ValueError(f"No extractable text found in '{filename}'. The PDF may be scanned/image-only and require OCR.")

    # Chroma DB Setup
    chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    # Using a tenant-specific collection for strict data isolation
    chroma_collection = chroma_client.get_or_create_collection(f"policy_documents_{institution_id}")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Chunking and Indexing
    embed_model = get_embedding_model()
    parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = parser.get_nodes_from_documents(llama_docs)

    VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model
    )

    return page_count