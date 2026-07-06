from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"

IMAGE_DIR = RAW_DIR / "images"

METADATA_FILE = RAW_DIR / "metadata.csv"

PROCESSED_DIR = DATA_DIR / "processed"

EMBEDDING_DIR = DATA_DIR / "embeddings"

INDEX_DIR = DATA_DIR / "indexes"

CACHE_DIR = DATA_DIR / "cache"