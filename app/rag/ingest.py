import pickle
from typing import List, Dict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import POLICIES_DIR, VECTORSTORE_DIR, FAISS_INDEX_PATH, DOCUMENTS_PATH


def split_text_into_chunks(
    text: str,
    chunk_size: int = 180,
    chunk_overlap: int = 40
) -> List[str]:
    """
    Split text into overlapping chunks based on words.

    Args:
        text: Full document text.
        chunk_size: Number of words per chunk.
        chunk_overlap: Number of overlapping words between consecutive chunks.

    Returns:
        List of chunk strings.
    """
    words = text.split()

    if not words:
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    step = chunk_size - chunk_overlap

    for start_idx in range(0, len(words), step):
        end_idx = start_idx + chunk_size
        chunk_words = words[start_idx:end_idx]

        if not chunk_words:
            continue

        chunk_text = " ".join(chunk_words).strip()
        if chunk_text:
            chunks.append(chunk_text)

        if end_idx >= len(words):
            break

    return chunks


def load_and_chunk_documents() -> List[Dict]:
    """
    Load markdown policy files and split them into chunks.
    Each chunk becomes an independent retrievable unit.
    """
    chunked_documents = []

    for path in POLICIES_DIR.glob("*.md"):
        with open(path, "r", encoding="utf-8") as f:
            full_text = f.read().strip()

        chunks = split_text_into_chunks(
            text=full_text,
            chunk_size=60,
            chunk_overlap=10
        )

        for chunk_id, chunk_text in enumerate(chunks):
            chunked_documents.append({
                "source": path.name,
                "chunk_id": chunk_id,
                "text": chunk_text
            })

    return chunked_documents


def build_vectorstore():
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    documents = load_and_chunk_documents()
    if not documents:
        raise ValueError(f"No policy documents found in: {POLICIES_DIR}")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts, convert_to_numpy=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))

    faiss.write_index(index, str(FAISS_INDEX_PATH))

    with open(DOCUMENTS_PATH, "wb") as f:
        pickle.dump(documents, f)

    print("Vectorstore created successfully.")
    print(f"Policies loaded from: {POLICIES_DIR}")
    print(f"Total chunks created: {len(documents)}")
    print(f"FAISS index saved to: {FAISS_INDEX_PATH}")
    print(f"Chunk metadata saved to: {DOCUMENTS_PATH}")


if __name__ == "__main__":
    build_vectorstore()