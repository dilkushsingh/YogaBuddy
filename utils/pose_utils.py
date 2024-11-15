import mediapipe as mp
import cv2

mp_pose = mp.solutions.pose
pose_detector = mp_pose.Pose(static_image_mode=True, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils

def detect_pose(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose_detector.process(rgb_frame)
    return results if results else False

def detect_keypoints(img):
    results = detect_pose(img)
    keypoints = {} 
    if results.pose_landmarks:
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            keypoints[idx] = (landmark.x, landmark.y, landmark.z)
    return keypoints

def draw_landmarks(frame):
    results = detect_pose(frame)
    return mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
def fetch_landmarks(frame):
    results = detect_pose(frame)
    draw_landmarks(frame)
    if results.pose_landmarks:
        row = []
        landmarks = results.pose_landmarks.landmark
        for landmark in landmarks:
            row.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
        return row