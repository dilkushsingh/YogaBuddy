import cv2
import mediapipe as mp
import pandas as pd
import os

class PoseProcessor:
    def __init__(self, input_path, output_path, min_detection_confidence=0.3, model_complexity=2):
        self.input_path = input_path
        self.output_path = output_path
        self.min_detection_confidence = min_detection_confidence
        self.model_complexity = model_complexity

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            min_detection_confidence=self.min_detection_confidence,
            model_complexity=self.model_complexity,
        )

        points = self.mp_pose.PoseLandmark
        self.columns = [f"{point.name}_{axis}" for point in points for axis in ["x", "y", "z", "vis"]]
        self.columns.append('class')

    def process_image(self, img_path, class_label):
        try:
            img = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.pose.process(img_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                row = []
                for landmark in landmarks:
                    row.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
                row.append(class_label)
                return row
        except:
            print(f"Error processing image {img_path}")
        return None

    def process_directory(self):
        data_rows = []
        for dir_name in os.listdir(self.input_path):
            label_dir = os.path.join(self.input_path, dir_name)
            class_label = dir_name

            if not os.path.isdir(label_dir):
                continue
            print(f"Processing class: {class_label}")

            for img_name in os.listdir(label_dir):
                img_path = os.path.join(label_dir, img_name)
                if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue

                row = self.process_image(img_path, class_label)
                if row:
                    data_rows.append(row)
        return data_rows

    def save_to_csv(self, data_rows):
        data = pd.DataFrame(data_rows, columns=self.columns)
        data.to_csv(self.output_path, index=False)

    def generate(self):
        data_rows = self.process_directory()
        self.save_to_csv(data_rows)

if __name__ == "__main__":
    input_dir = 'data/sun_salutation_poses/train/'
    output_dir = 'data/train.csv'
    pose_processor = PoseProcessor(input_dir, output_dir)
    pose_processor.generate()