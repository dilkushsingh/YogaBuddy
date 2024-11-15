import numpy as np
import cv2
import joblib
import mediapipe as mp
from utils.pose_utils import detect_pose, draw_landmarks, fetch_landmarks
from constant import MODEL_PATH

mp_pose = mp.solutions.pose
pose_detector = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def load_model(model_path):
    model = joblib.load(model_path)
    return model

model = load_model(MODEL_PATH)

classes_ = np.array(['Ashtanga Namaskara', 'Ashwa Sanchalanasana', 'Bhujangasana', 'Hasta Uttanasana', 'Parvatasana', 'Pranamasana', 'Uttanasana'])

def classify_pose(frame):
    try:
        row = fetch_landmarks(frame)
        batch = np.expand_dims(row, axis=0)
        predictions = model.predict(batch)
        pose_name = classes_[predictions]
        return pose_name
    except:
        return None
