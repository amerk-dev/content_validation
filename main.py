import io
import hashlib
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from cachetools import Cache
import cv2
import tensorflow as tf

from validate import detect_photo, detect_video, validate_text
from schemas import Content, ContentCrud, Text, TextCrud

app = FastAPI()
cache = Cache(maxsize=1000)


def hash_data(data):
    return hashlib.sha256(data).hexdigest()


@app.post("/detect/photo/", response_model=Content)
async def classify_image(file: UploadFile = File(...)):
    image_data = await file.read()
    image_hash = hash_data(image_data)

    if image_hash in cache: return cache[image_hash]

    image = Image.open(io.BytesIO(image_data))
    validation_data = detect_photo(image)

    content_data = Content(
        file_name=file.filename,
        is_nsfw=validation_data["is_nsfw"],
        confidence_percentage=validation_data["confidence_percentage"],
        content_type="photo"
    )
    new_record = ContentCrud().add(content_data)
    cache[image_hash] = content_data
    return new_record


@app.post("/detect/video/", response_model=Content)
async def classify_video(file: UploadFile):
    video_data = await file.read()
    video_hash = hash_data(video_data)

    if video_hash in cache:
        return cache[video_hash]

    validation_data = detect_video(video_data)
    content_data = Content(
        file_name=file.filename,
        is_nsfw=validation_data["is_nsfw"],
        confidence_percentage=validation_data["confidence_percentage"],
        content_type="video"
    )
    new_record = ContentCrud().add(content_data)

    cache[video_hash] = content_data
    return new_record


@app.post("/text-validation/", response_model=Text)
async def text_validation(title: str, description: str):
    text_crud = TextCrud()
    res = await validate_text(text_to_validate=description)
    content_data = Text(
        title=title,
        description=description,
        valid=res
    )

    new_record = text_crud.add(content_data)
    return new_record


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
