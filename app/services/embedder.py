from pathlib import Path

from PIL import Image
from sentence_transformers import SentenceTransformer
import torch
from transformers import CLIPModel, CLIPProcessor

TEXT_MODEL_NAME = "all-MiniLM-L6-v2"
IMAGE_MODEL_NAME = "openai/clip-vit-base-patch32"

text_model = SentenceTransformer(TEXT_MODEL_NAME)
clip_model = CLIPModel.from_pretrained(IMAGE_MODEL_NAME)
clip_processor = CLIPProcessor.from_pretrained(IMAGE_MODEL_NAME)


def embed_text(text: str) -> list[float]:
    cleaned_text = text.strip()
    if not cleaned_text:
        raise ValueError("Text content must not be empty.")

    embedding = text_model.encode(cleaned_text, normalize_embeddings=True)
    return embedding.tolist()


def embed_image(image_path: str | Path) -> list[float]:
    path = Path(image_path)
    if not path.exists():
        raise ValueError("Image file does not exist.")

    with Image.open(path) as image:
        rgb_image = image.convert("RGB")
        inputs = clip_processor(images=rgb_image, return_tensors="pt")

    with torch.no_grad():
        image_features = clip_model.get_image_features(**inputs)
        image_features = torch.nn.functional.normalize(image_features, p=2, dim=-1)

    return image_features[0].cpu().tolist()
