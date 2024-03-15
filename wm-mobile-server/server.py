import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import io
import numpy as np
import tensorflow as tf
from PIL import Image

from flask import Flask, request, jsonify

unique_labels = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

IMG_SIZE = 224


def process_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")
    image = image.resize((IMG_SIZE, IMG_SIZE))
    image = np.array(image) / 255.0  # Normalize image
    return image.astype(np.float32)  # Convert to float32


# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="model-phone.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})
        try:
            image_bytes = file.read()
            # Preprocess image
            image = process_image(image_bytes)
            # Run inference
            interpreter.set_tensor(
                input_details[0]["index"], np.expand_dims(image, axis=0)
            )
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]["index"])
            pred_labels = unique_labels[np.argmax(output_data[0])]

            data = {"prediction": pred_labels}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
