from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
POLICIES_DIR = DATA_DIR / "policies"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

FAISS_INDEX_PATH = VECTORSTORE_DIR / "faiss_index.bin"
DOCUMENTS_PATH = VECTORSTORE_DIR / "documents.pkl"

TICKETS_PATH = DATA_DIR / "tickets.json"

# LLM settings
MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
MAX_NEW_TOKENS = 200
TEMPERATURE = 0.3
TOP_P = 0.9