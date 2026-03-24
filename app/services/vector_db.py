from pathlib import Path
from typing import Any

import chromadb

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DB_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "knowledge_base"

CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def add_embedding(file_id: str, embedding: list[float], metadata: dict[str, Any]) -> None:
    collection.upsert(
        ids=[file_id],
        embeddings=[embedding],
        metadatas=[metadata],
    )


def search_embeddings(query_embedding: list[float], n_results: int = 5) -> list[dict[str, Any]]:
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["metadatas", "distances"],
    )

    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    formatted_results: list[dict[str, Any]] = []
    for metadata, distance in zip(metadatas, distances):
        safe_metadata = metadata or {}
        similarity_score = max(0.0, 1.0 - float(distance))

        formatted_results.append(
            {
                "file_name": safe_metadata.get("file_name"),
                "file_type": safe_metadata.get("file_type"),
                "similarity_score": round(similarity_score, 4),
                "metadata": safe_metadata,
            }
        )

    return formatted_results
