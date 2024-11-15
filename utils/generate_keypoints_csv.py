import cv2
import numpy as np
import mediapipe as mp
import pandas as pd
import os

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils

path = 'data/sun_salutation_poses/test/'
points = mp_pose.PoseLandmark
columns = [f"{mp_pose.PoseLandmark(point).name}_{axis}" for point in points for axis in ["x", "y", "z", "vis"]]
columns.append('class')
data = pd.DataFrame(columns=columns)

count = 0
for dir_name in os.listdir(path):
    label_dir = os.path.join(path, dir_name)
    class_label = dir_name

    if not os.path.isdir(label_dir):
        continue
    
    for img_name in os.listdir(label_dir):
        img_path = os.path.join(label_dir, img_name)
        
        if not (img_name.endswith('.jpg') or img_name.endswith('.jpeg') or img_name.endswith('.png')):
            continue
        
        try:
            img = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                row = []
                for landmark in landmarks:
                    row.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
                row.append(class_label)
                data.loc[count] = row
                count += 1

        except Exception as e:
            print(f"Error processing image {img_name} in {dir_name}: {e}")
            continue

data.to_csv('data/test.csv', index=False)