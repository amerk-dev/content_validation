import io
import hashlib
import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from transformers import pipeline
from transformers.pipelines import PipelineException
from PIL import Image
from cachetools import Cache
import tensorflow as tf


app = FastAPI()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

cache = Cache(maxsize=1000)

model = pipeline("image-classification", model="falconsai/nsfw_image_detection")

DEVICE = "GPU" if tf.config.list_physical_devices('GPU') else "CPU"
logging.info("TensorFlow version: %s", tf.__version__)
logging.info("Model is using: %s", DEVICE)


if DEVICE == "GPU":
    logging.info("GPUs available: %d", len(tf.config.list_physical_devices("GPU")))

def hash_data(data):
    return hashlib.sha256(data).hexdigest()


@app.post("/detect")
async def classify_image(file: UploadFile = File(...)):
    try:
        logging.info("Processing %s", file.filename)
        image_data = await file.read()
        image_hash = hash_data(image_data)

        if image_hash in cache:
            logging.info("Returning cached entry for %s", file.filename)
            return JSONResponse(status_code=200, content=cache[image_hash])

        image = Image.open(io.BytesIO(image_data))

        results = model(image)


        best_prediction = max(results, key=lambda x: x["score"])

        confidence_percentage = round(best_prediction["score"] * 100, 1)


        response_data = {
            "file_name": file.filename,
            "is_nsfw": best_prediction["label"] == "nsfw",
            "confidence_percentage": confidence_percentage,
        }

        cache[image_hash] = response_data

        return JSONResponse(status_code=200, content=response_data)

    except PipelineException as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
