import cv2
import mediapipe as mp
import numpy as np
import joblib
import math

class Pose:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose_detector = self.mp_pose.Pose(static_image_mode=True, model_complexity=2, model_path='models/pose_landmark_full.tflite')
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_pose(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.pose_detector.process(rgb_frame)

    def get_keypoints(self, frame):
        results = self.detect_pose(frame)
        keypoints = {}
        if results.pose_landmarks:
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                keypoints[idx] = (landmark.x, landmark.y, landmark.z)
        return keypoints

    def calculate_angle(self, a, b, c):
        ba = np.array([a[0] - b[0], a[1] - b[1], a[2] - b[2]])
        bc = np.array([c[0] - b[0], c[1] - b[1], c[2] - b[2]])
        dot_product = np.dot(ba, bc)
        magnitude = np.linalg.norm(ba) * np.linalg.norm(bc)
        angle_rad = math.acos(dot_product / magnitude) if magnitude != 0 else 0
        return math.degrees(angle_rad)

    def draw_landmarks(self, frame, landmarks=None):
        results = self.detect_pose(frame) if landmarks is None else landmarks
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        
    def fetch_landmarks(self, frame):
        results = self.detect_pose(frame)
        self.draw_landmarks(frame)
        if results.pose_landmarks:
            row = []
            landmarks = results.pose_landmarks.landmark
            for landmark in landmarks:
                row.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
            return row

class Classifier(Pose):
    def __init__(self, model_path, pose_classes):
        super().__init__()
        self.model = joblib.load(model_path)
        self.classes = np.array(pose_classes)

    def classify_pose(self, frame):
        try:
            row = self.fetch_landmarks(frame)
            batch = np.expand_dims(row, axis=0)
            predictions = self.model.predict(batch)
            return self.classes[predictions]
        except:
            return None
        
class Comparison(Pose):
    def __init__(self, angle_threshold):
        super().__init__()
        self.angle_threshold = angle_threshold

    def calculate_angles(self, keypoints):
        landmarks = self.mp_pose.PoseLandmark
        angles = {}
        angles['left_elbow'] = self.calculate_angle(
            keypoints[landmarks.LEFT_SHOULDER.value],
            keypoints[landmarks.LEFT_ELBOW.value],
            keypoints[landmarks.LEFT_WRIST.value]
        )
        angles['right_elbow'] = self.calculate_angle(
            keypoints[landmarks.RIGHT_SHOULDER.value],
            keypoints[landmarks.RIGHT_ELBOW.value],
            keypoints[landmarks.RIGHT_WRIST.value]
        )
        angles['left_shoulder'] = self.calculate_angle(
            keypoints[landmarks.LEFT_ELBOW.value],
            keypoints[landmarks.LEFT_SHOULDER.value],
            keypoints[landmarks.LEFT_HIP.value]
        )
        angles['right_shoulder'] = self.calculate_angle(
            keypoints[landmarks.RIGHT_ELBOW.value],
            keypoints[landmarks.RIGHT_SHOULDER.value],
            keypoints[landmarks.RIGHT_HIP.value]
        )
        angles['left_hip'] = self.calculate_angle(
            keypoints[landmarks.LEFT_KNEE.value],
            keypoints[landmarks.LEFT_HIP.value],
            keypoints[landmarks.LEFT_SHOULDER.value]
        )
        angles['right_hip'] = self.calculate_angle(
            keypoints[landmarks.RIGHT_KNEE.value],
            keypoints[landmarks.RIGHT_HIP.value],
            keypoints[landmarks.RIGHT_SHOULDER.value]
        )
        angles['left_knee'] = self.calculate_angle(
            keypoints[landmarks.LEFT_HIP.value],
            keypoints[landmarks.LEFT_KNEE.value],
            keypoints[landmarks.LEFT_ANKLE.value]
        )
        angles['right_knee'] = self.calculate_angle(
            keypoints[landmarks.RIGHT_HIP.value],
            keypoints[landmarks.RIGHT_KNEE.value],
            keypoints[landmarks.RIGHT_ANKLE.value]
        )
        angles['left_ankle'] = self.calculate_angle(
            keypoints[landmarks.LEFT_KNEE.value],
            keypoints[landmarks.LEFT_ANKLE.value],
            keypoints[landmarks.LEFT_FOOT_INDEX.value]
        )
        angles['right_ankle'] = self.calculate_angle(
            keypoints[landmarks.RIGHT_KNEE.value],
            keypoints[landmarks.RIGHT_ANKLE.value],
            keypoints[landmarks.RIGHT_FOOT_INDEX.value]
        )
        angles['left_wrist'] = self.calculate_angle(
            keypoints[landmarks.LEFT_ELBOW.value],
            keypoints[landmarks.LEFT_WRIST.value],
            keypoints[landmarks.LEFT_PINKY.value]
        )
        angles['right_wrist'] = self.calculate_angle(
            keypoints[landmarks.RIGHT_ELBOW.value],
            keypoints[landmarks.RIGHT_WRIST.value],
            keypoints[landmarks.RIGHT_PINKY.value]
        )
        return angles
    
    def process_frames(self, frame):
        keypoints = self.get_keypoints(frame)
        angles = self.calculate_angles(keypoints)
        return keypoints, angles

    def compare_poses(self, ideal_angles, user_angles):
        feedback = {}
        for joint, ideal_angle in ideal_angles.items():
            user_angle = user_angles.get(joint, None)
            if user_angle is None and ideal_angle is None:
                feedback[joint] = 'angle not found'
            elif abs(ideal_angle - user_angle) <= self.angle_threshold:
                feedback[joint] = 'Correct'
            else:
                feedback[joint] = 'Incorrect'
        return feedback

    def draw_feedback(self, frame, feedback, keypoints):
        scaling_factor = max(frame.shape[0], frame.shape[1]) / 1000
        for joint, status in feedback.items():
            idx = self.mp_pose.PoseLandmark[joint.upper()].value
            x, y, z = keypoints[idx]
            x = int(x * frame.shape[1])
            y = int(y * frame.shape[0])
            color = (0, 255, 0) if status == 'Correct' else (0, 0, 255)
            base_radius = 5
            radius = max(2, int(base_radius * scaling_factor * (1-z)))
            cv2.circle(frame, (x, y), radius, color, -1)
        return frame

    def practice_pose(self, ideal_frame, user_frame):
        ideal_keypoints, ideal_angles = self.process_frames(ideal_frame)
        user_keypoints, user_angles = self.process_frames(user_frame)
        feedback = self.compare_poses(ideal_angles, user_angles)
        result_frame = self.draw_feedback(user_frame, feedback, user_keypoints)
        return result_frame
