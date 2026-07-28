import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ==========================
# API Keys
# ==========================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# ==========================
# Project Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

PDF_PATH = RAW_DATA_DIR / "study_material.pdf"

VECTOR_DB_PATH = DATA_DIR / "vector_store"

LOG_DIR = BASE_DIR / "logs"


# ==========================
# RAG Settings
# ==========================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

TOP_K_RESULTS = 5


MODEL_NAME = "meta-llama/llama-3.1-8b-instruct"

TEMPERATURE = 0.2