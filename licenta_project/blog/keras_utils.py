import os
import json
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from keras.models import load_model
from django.conf import settings

MODEL_DIR = os.path.join(settings.BASE_DIR, 'classifier')

model_path = os.path.join(MODEL_DIR, 'Modul-5-iunie.keras')
labels_path = os.path.join(MODEL_DIR, 'class_labels.json')

print(f"Loading model from: {model_path}")
model = load_model(model_path)

with open(labels_path, 'r') as f:
    class_labels = json.load(f)

def warm_up_model():
    """Rulează o predicție dummy pentru a inițializa modelul în memorie"""
    try:
        dummy_img = np.random.random((1, 260, 260, 3))
        dummy_img = preprocess_input(dummy_img)
        model.predict(dummy_img)
        print("Model warmed up successfully!")
    except Exception as e:
        print(f"Warm up failed: {e}")

def classify_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(260, 260))
        
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        preds = model.predict(img_array)[0]
        predicted_index = np.argmax(preds)
        
        label = class_labels[str(predicted_index)] if str(predicted_index) in class_labels else class_labels[predicted_index]
        confidence = float(preds[predicted_index])
        
        return label, confidence
    except Exception as e:
        print(f"Error in classification: {e}")
        return "error", 0.0