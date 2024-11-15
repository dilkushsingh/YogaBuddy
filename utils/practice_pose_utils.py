import numpy as np
import cv2
import mediapipe as mp
import math
from utils.pose_utils import detect_pose, detect_keypoints
from constant import ANGLE_THRESHOLD

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2) 
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    ba = np.array([a[0]-b[0], a[1]-b[1], a[2]-b[2]])
    bc = np.array([c[0]-b[0], c[1]-b[1], c[2]-b[2]])

    dot_prod = np.dot(ba, bc)
    mag_ba = np.linalg.norm(ba)
    mag_bc = np.linalg.norm(bc)

    angle_rad = math.acos(dot_prod / (mag_ba * mag_bc))
    angle_deg = math.degrees(angle_rad)
    return angle_deg

def calculate_angles(keypoints):
    angles = {}
    angles['left_elbow'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
        keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value],
        keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value]
    )
    angles['right_elbow'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    )
    angles['left_shoulder'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value],
        keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
        keypoints[mp_pose.PoseLandmark.LEFT_HIP.value]
    )
    angles['right_shoulder'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value]
    )
    angles['left_hip'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value],
        keypoints[mp_pose.PoseLandmark.LEFT_HIP.value],
        keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    )
    angles['right_hip'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    )
    angles['left_knee'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.LEFT_HIP.value],
        keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value],
        keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    )
    angles['right_knee'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
    )
    angles['left_ankle'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value],
        keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value],
        keypoints[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
    )
    angles['right_ankle'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
    )
    angles['left_wrist'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value],
        keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value],
        keypoints[mp_pose.PoseLandmark.LEFT_PINKY.value]
    )
    angles['right_wrist'] = calculate_angle(
        keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value],
        keypoints[mp_pose.PoseLandmark.RIGHT_PINKY.value]
    )
    return angles

def process_frames(frame):
    keypoints = detect_keypoints(frame)
    angles = calculate_angles(keypoints)
    return keypoints, angles

def compare_poses(ideal_angles, user_angles):
    feedback = {}
    for joint, angle in ideal_angles.items():
        threshold = ANGLE_THRESHOLD
        ideal_angle = ideal_angles.get(joint, None)
        user_angle = user_angles.get(joint, None)
        if ideal_angle is None:
            feedback[joint] = 'Ideal angle not found'
        elif user_angle is None:
            feedback[joint] = 'User angle not found'
        else:
            if abs(ideal_angle-user_angle) <= threshold:
                feedback[joint] = 'Correct'
            else:
                feedback[joint] = 'Incorrect'
    return feedback

def draw_feedback_on_frame(frame, feedback, keypoints):
    scaling_factor = max(frame.shape[0], frame.shape[1]) / 1000
    
    for joint, status in feedback.items():
        joint_idx = mp_pose.PoseLandmark[joint.upper()].value
        if joint_idx in keypoints:
            x, y, z = keypoints[joint_idx]
            x = int(x * frame.shape[1])
            y = int(y * frame.shape[0])

            color = (0, 255, 0) if status == 'Correct' else (0, 0, 255)

            base_radius = 5
            radius = max(2, int(base_radius * scaling_factor * (1 - z)))  
            cv2.circle(frame, (x, y), radius, color, -1)
    return frame