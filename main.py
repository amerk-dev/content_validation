import io
import hashlib
import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from transformers import pipeline
from transformers.pipelines import PipelineException
from PIL import Image
from cachetools import Cache
import cv2
import tensorflow as tf

from validate import detect_photo


app = FastAPI()
cache = Cache(maxsize=1000)


def hash_data(data):
    return hashlib.sha256(data).hexdigest()


@app.post("/detect/photo")
async def classify_image(file: UploadFile = File(...)):
    image_data = await file.read()
    image_hash = hash_data(image_data)

    if image_hash in cache: return cache[image_hash]

    image = Image.open(io.BytesIO(image_data))
    validation_data = detect_photo(image)
    response_data = {
        "file_name": file.filename,
        "is_nsfw": validation_data["is_nsfw"],
        "confidence_percentage": validation_data["confidence_percentage"],
    }

    cache[image_hash] = response_data
    return response_data

@app.post("/detect/video/")
async def classify_video(file: UploadFile = File(...)):
    video_data = await file.read()
    video_hash = hash_data(video_data)

    if video_hash in cache:
        return cache[video_hash]

    video_capture = cv2.VideoCapture(video_data)

    # Устанавливаем счетчик кадров и счетчик времени
    frame_count = 0
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    interval = int(frame_rate)

    # Читаем кадры до тех пор, пока они доступны
    while video_capture.isOpened():
        # Пропускаем кадры до нужного момента
        for _ in range(interval - 1):
            video_capture.grab()

        # Читаем следующий кадр
        ret, frame = video_capture.read()

        # Проверяем, был ли успешно прочитан кадр
        if not ret:
            break

        #


        # Увеличиваем счетчик кадров
        frame_count += 1

    # Закрываем видео файл
    video_capture.release()

    return {"Response": "all ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
