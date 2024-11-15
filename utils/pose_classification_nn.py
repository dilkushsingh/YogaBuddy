import numpy as np
import cv2
import tensorflow
from tensorflow.keras.models import load_model
from constant import KERAS_MODEL_PATH

model = load_model(KERAS_MODEL_PATH)

pose_labels = ['AshtangaNamaskara', 'AshwaSanchalanasana', 'Bhujangasana', 'HastaUttanasana', 'Parvatasana', 'Pranamasana', 'Uttanasana']

def image_processing(frame):
    img = cv2.resize(frame, (224, 224))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def classify_pose(frame):
    img = image_processing(frame)

    predictions = model.predict(img)
    class_idx = np.argmax(predictions, axis=1)[0]
    pose_name = pose_labels[class_idx]
    return pose_name