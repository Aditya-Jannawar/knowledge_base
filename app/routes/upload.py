from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.services.embedder import embed_image, embed_text
from app.services.file_handler import FileValidationError, save_upload_file
from app.services.vector_db import add_embedding

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    try:
        saved_file = await save_upload_file(file)
    except FileValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    try:
        if saved_file.file_type == "text":
            content = saved_file.path.read_text(encoding="utf-8")
            embedding = embed_text(content)
        else:
            embedding = embed_image(saved_file.path)

        add_embedding(
            file_id=saved_file.file_id,
            embedding=embedding,
            metadata={
                "file_name": saved_file.original_name,
                "stored_file_name": saved_file.stored_name,
                "file_type": saved_file.file_type,
                "file_path": str(saved_file.path),
            },
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process and index file.",
        ) from exc

    return {
        "id": saved_file.file_id,
        "file_name": saved_file.original_name,
        "file_type": saved_file.file_type,
    }
