import pickle
from typing import List, Dict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import FAISS_INDEX_PATH, DOCUMENTS_PATH


class PolicyRetriever:
    def __init__(self):
        if not FAISS_INDEX_PATH.exists():
            raise FileNotFoundError(
                f"FAISS index not found at {FAISS_INDEX_PATH}. "
                "Run python -m app.rag.ingest first."
            )

        if not DOCUMENTS_PATH.exists():
            raise FileNotFoundError(
                f"Documents file not found at {DOCUMENTS_PATH}. "
                "Run python -m app.rag.ingest first."
            )

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))

        with open(DOCUMENTS_PATH, "rb") as f:
            self.documents = pickle.load(f)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        query_embedding = self.model.encode([query], convert_to_numpy=True)

        distances, indices = self.index.search(
            query_embedding.astype(np.float32),
            top_k
        )

        results = []
        for rank, idx in enumerate(indices[0]):
            if idx != -1:
                doc = self.documents[idx].copy()
                doc["distance"] = float(distances[0][rank])
                results.append(doc)

        return results