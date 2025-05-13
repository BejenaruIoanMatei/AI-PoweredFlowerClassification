import numpy as np
from tensorflow.keras.preprocessing import image
from keras.models import load_model
import os
import json

model_path = '/Users/user/Documents/GitHub/LucrareLicenta-FII-UAIC/classifier/2-Mai/Modul-2-Mai.keras'
model = load_model(model_path)

with open('/Users/user/Documents/GitHub/LucrareLicenta-FII-UAIC/classifier/2-Mai/class_labels.json') as f:
    class_labels = json.load(f)

def classify_image(img_path):
    try:
        print(f"📷 Clasific imaginea: {img_path}")
        img = image.load_img(img_path, target_size=(256, 256))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        preds = model.predict(img_array)[0]
        predicted_index = np.argmax(preds)
        label = class_labels[predicted_index]
        confidence = float(preds[predicted_index])
        print(f"✅ Predicted: {label} with confidence {confidence:.2f}")
        return label, confidence

    except Exception as e:
        print(f"Error in classification: {e}")
        return "error", 0.0
