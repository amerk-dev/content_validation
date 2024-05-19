import cv2
from transformers import pipeline
from PIL import Image

from schemas import Content, ContentCrud, Text, TextCrud


model = pipeline("image-classification", model="falconsai/nsfw_image_detection")

def frame_to_pil_image(frame):
    # OpenCV возвращает изображение в формате BGR, а PIL требует RGB, поэтому нужно поменять цветовые каналы
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    return pil_image

def detect_photo(image):
    results = model(image)
    best_prediction = max(results, key=lambda x: x["score"])
    confidence_percentage = round(best_prediction["score"] * 100, 1)
    data = {
        "is_nsfw": best_prediction["label"] == "nsfw",
        "confidence_percentage": confidence_percentage,
    }

    return data

def detect_video(video):
    data = {
        "is_nsfw": False,
        "confidence_percentage": 0,
    }

    with open("../temp_video.mp4", "wb") as temp_file:
        temp_file.write(video)

    video_capture = cv2.VideoCapture("../temp_video.mp4")

    frame_count = 0
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    interval = int(frame_rate)

    while video_capture.isOpened():
        for _ in range(interval - 1):
            video_capture.grab()

        ret, frame = video_capture.read()

        # Проверяем, был ли успешно прочитан кадр
        if not ret:
            break

        pil_frame = frame_to_pil_image(frame)
        frame_nsfw = model(pil_frame)
        print(frame_nsfw)
        best_prediction = max(frame_nsfw, key=lambda x: x["score"])
        confidence_percentage = round(best_prediction["score"] * 100, 1)
        if best_prediction["label"] == "nsfw":
            data["is_nsfw"] = best_prediction["label"] == "nsfw"
            data["confidence_percentage"] = confidence_percentage
            break
        frame_count += 1

    # Закрываем видео файл
    video_capture.release()
    print(data)
    return data