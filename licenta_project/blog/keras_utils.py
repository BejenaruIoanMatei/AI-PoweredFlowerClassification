import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from keras.models import load_model
import os
import json

model_path = '/Users/user/Documents/GitHub/LucrareLicenta-FII-UAIC/classifier/5-iunie/Modul-5-iunie.keras'
model = load_model(model_path)

with open('/Users/user/Documents/GitHub/LucrareLicenta-FII-UAIC/classifier/5-iunie/class_labels.json') as f:
    class_labels = json.load(f)

def warm_up_model():
    dummy_img = np.random.random((1, 260, 260, 3))
    dummy_img = preprocess_input(dummy_img)
    
    model.predict(dummy_img)
    print("Model warmed up successfully!")
    
def classify_image(img_path):
    try:
        print(f"Clasific imaginea: {img_path}")
        img = image.load_img(img_path, target_size=(260, 260))
        
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        preds = model.predict(img_array)[0]
        predicted_index = np.argmax(preds)
        
        label = class_labels[predicted_index]
        confidence = float(preds[predicted_index])
        
        print(f"Predicted: {label} with confidence {confidence:.2f}")
        return label, confidence
    except Exception as e:
        print(f"Error in classification: {e}")
        return "error", 0.0
