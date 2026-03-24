from fastapi import APIRouter, HTTPException, Query, status
from app.services.embedder import embed_text
from app.services.vector_db import search_embeddings

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search(query: str = Query(..., min_length=1), limit: int = Query(5, ge=1, le=20)):
    cleaned_query = query.strip()
    if not cleaned_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query must not be empty.",
        )

    try:
        query_embedding = embed_text(cleaned_query)
        results = search_embeddings(query_embedding=query_embedding, n_results=limit)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search indexed files.",
        ) from exc

    return {
        "query": cleaned_query,
        "count": len(results),
        "results": results,
    }
