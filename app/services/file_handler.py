import re
import uuid
from dataclasses import dataclass
from pathlib import Path

from fastapi import UploadFile

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

TEXT_EXTENSIONS = {".txt", ".md"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
ALLOWED_EXTENSIONS = TEXT_EXTENSIONS | IMAGE_EXTENSIONS


class FileValidationError(ValueError):
    pass


@dataclass(slots=True)
class SavedFile:
    file_id: str
    original_name: str
    stored_name: str
    file_type: str
    path: Path


def _sanitize_filename(filename: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]", "_", filename).strip("._")
    return sanitized or "file"


def _resolve_file_type(extension: str) -> str:
    if extension in TEXT_EXTENSIONS:
        return "text"
    if extension in IMAGE_EXTENSIONS:
        return "image"
    raise FileValidationError(
        f"Unsupported file type '{extension}'. Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}."
    )


async def save_upload_file(file: UploadFile) -> SavedFile:
    if not file.filename:
        raise FileValidationError("Missing file name.")

    extension = Path(file.filename).suffix.lower()
    file_type = _resolve_file_type(extension)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_id = str(uuid.uuid4())
    safe_name = _sanitize_filename(Path(file.filename).stem)
    stored_name = f"{file_id}_{safe_name}{extension}"
    destination = DATA_DIR / stored_name

    content = await file.read()
    if not content:
        raise FileValidationError("Uploaded file is empty.")

    destination.write_bytes(content)
    await file.close()

    return SavedFile(
        file_id=file_id,
        original_name=file.filename,
        stored_name=stored_name,
        file_type=file_type,
        path=destination,
    )
