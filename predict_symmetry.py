import tensorflow as tf
import numpy as np
import cv2

CLASS_NAMES = ["asymmetric", "both", "reflection", "rotation"]

model = tf.keras.models.load_model("kolam_symmetry_cnn.h5")

def predict_kolam_symmetry(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (128, 128))
    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)
    idx = np.argmax(preds)

    return {
        "predicted_symmetry": CLASS_NAMES[idx],
        "confidence": float(preds[0][idx])
    }
