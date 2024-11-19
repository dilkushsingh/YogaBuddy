import numpy as np
import cv2
import streamlit as st
from utils.pose_utils import Classifier
from utils.streamlit_helpers import fetch_image
from constant import CLASSIFY_TITLE, UPLOAD_ISSUE, POSE_NOT_DETECTED_ISSUE, CAMERA_ISSUE, CAMERA_NOT_DETECTED_ISSUE

class PoseClassifier:
    def __init__(self, model_path, pose_classes):
        self.cap = None 
        self.classifier = Classifier(model_path, pose_classes)

    def classify_by_image(self):
        try:
            frame = fetch_image()
            if frame is not None:
                if st.button('Detect Pose'):
                    pose_name = self.classifier.classify_pose(frame)[0]
                    st.write('Your current pose is:')
                    st.success(pose_name)
                    st.image(frame, channels="BGR")
        except:
            st.error(UPLOAD_ISSUE)

    def classify_by_feed(self):
        try:
            start_camera = st.button("Start Camera", key="start")
            stop_camera = st.button("Stop Camera", key="stop")

            if start_camera and not stop_camera:
                self.cap = cv2.VideoCapture(0)
                status = st.empty()
                pose_placeholder = st.empty()
                st_frame = st.empty()

                while self.cap.isOpened():
                    ret, frame = self.cap.read()
                    if not ret:
                        st.write(CAMERA_NOT_DETECTED_ISSUE)
                        break

                    frame = cv2.flip(frame, 1) 
                    try:
                        pose_name = self.classifier.classify_pose(frame)[0]
                        status.write('Your current pose is:')
                        pose_placeholder.success(pose_name)
                    except:
                        status.error(POSE_NOT_DETECTED_ISSUE)
                        pose_placeholder.empty()

                    st_frame.image(frame, channels="BGR")

                    if stop_camera:
                        self.cap.release()
                        break
        except:
            st.error(CAMERA_ISSUE)

    def display(self):
        st.title(CLASSIFY_TITLE)
        classify_option = st.radio("Choose input method:", ["Upload Image", "Live Camera"])

        if classify_option == "Upload Image":
            self.classify_by_image()
        elif classify_option == "Live Camera":
            self.classify_by_feed()
