from pathlib import Path

from app.ingestion.load_gitlab import IngestionConfig
from app.ingestion.build_index import build_chroma_index

ROOT = Path(__file__).resolve().parents[1]

cfg = IngestionConfig(
    people_dir=ROOT / "handbook-src" / "content" / "handbook" / "people-group",
    security_dir=ROOT / "handbook-src" / "content" / "handbook" / "security",
    people_limit=30,
    security_limit=70,
)

build_chroma_index(
    cfg=cfg,
    persist_dir=ROOT / "data" / "chroma",
    collection_name="gitlab_handbook_mvp",
)