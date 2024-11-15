import cv2
import mediapipe as mp
import numpy as np
from constant import DISTANCE_THRESHOLD

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils

ideal_img = cv2.imread('data/sun_salutation_poses/test/Bhujangasana/16102003_2564.jpg', cv2.COLOR_BGR2RGB)
results = pose.process(ideal_img)
ideal_keypoints = results.pose_landmarks

user_img = cv2.imread('data/sun_salutation_poses/test/Bhujangasana/16102003_2508.jpg', cv2.COLOR_BGR2RGB)
user_results = pose.process(user_img)
user_keypoints = user_results.pose_landmarks

def compare_keypoint_distances(user_img, user_keypoints, ideal_keypoints):
    if user_keypoints and ideal_keypoints:
        feedback = {}
        threshold = DISTANCE_THRESHOLD
        temp_img = user_img.copy()
        for idx, landmark in enumerate(user_keypoints.landmark):
            ideal_landmark = ideal_keypoints.landmark[idx]
            dist = np.linalg.norm(np.array([landmark.x, landmark.y]) - np.array([ideal_landmark.x, ideal_landmark.y])) 
            color = (0, 255, 0) if dist < threshold else (0, 0, 255)
            feedback[idx] = color

        circle_radius = max(3, int(user_img.shape[0] * 0.01))
        for idx, landmark in enumerate(user_keypoints.landmark):
            x, y = int(landmark.x * user_img.shape[1]), int(landmark.y * user_img.shape[0])
            cv2.circle(temp_img, (x,y), circle_radius, feedback[idx], -1)

        return temp_img
    else:
        return 'Keypoints are not detected'

output_img = compare_keypoint_distances(user_img, user_keypoints,ideal_keypoints)

cv2.imshow("User Pose Comparison Result", output_img)
cv2.waitKey(0)
cv2.destroyAllWindows()