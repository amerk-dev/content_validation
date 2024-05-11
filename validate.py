import cv2
from transformers import pipeline

model = pipeline("image-classification", model="falconsai/nsfw_image_detection")
def detect_photo(image):
    results = model(image)
    best_prediction = max(results, key=lambda x: x["score"])
    confidence_percentage = round(best_prediction["score"] * 100, 1)
    data = {
        "is_nsfw": best_prediction["label"] == "nsfw",
        "confidence_percentage": confidence_percentage,
    }

    return data

