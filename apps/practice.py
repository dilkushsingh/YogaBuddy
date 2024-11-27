import numpy as np
import cv2
import streamlit as st
import time
from constant import PRACTICE_TITLE, IDEAL_POSE_PATH, ANGLE_THRESHOLD, USER_MSG, UPLOAD_ISSUE, CAMERA_NOT_DETECTED_ISSUE, CAMERA_ISSUE, POSE_NOT_DETECTED_ISSUE
from utils.pose_utils import Comparison
from utils.streamlit_helpers import fetch_image

class PosePractice:
    def __init__(self, angle_threshold, s3utils):
        self.cap = None  
        self.comparison = Comparison(angle_threshold)
        self.s3utils = s3utils

    def fetch_ideal_pose(self):
        ideal_poses = list(IDEAL_POSE_PATH.keys())
        selected_pose = st.selectbox('Select an Ideal Pose', ideal_poses)
        ideal_pose_path = IDEAL_POSE_PATH[selected_pose]
        return ideal_pose_path

    def practice_by_image(self):
        try:
            col1, col2 = st.columns(2)
            with col1:
                ideal_frame_path = self.fetch_ideal_pose()
                ideal_frame = self.s3utils.fetch_image(ideal_frame_path)
                if ideal_frame is not None:
                    st.image(ideal_frame, channels='BGR', use_column_width=True)
                st.info(USER_MSG)

            user_frame = None
            with col2:
                user_frame = fetch_image()
                if ideal_frame is not None and user_frame is not None:
                    compare = st.button('Compare Pose')
                    if compare: 
                        result_img = self.comparison.practice_pose(ideal_frame, user_frame)
                        st.image(result_img, channels='BGR', use_column_width=True)
        except:
            with col2:
                st.error(UPLOAD_ISSUE)

    def practice_by_feed(self):
        try:
            col1, col2 = st.columns(2)

            with col1:
                ideal_frame_path = self.fetch_ideal_pose()
                ideal_frame = self.s3utils.fetch_image(ideal_frame_path)
                if ideal_frame is not None:
                    st.image(ideal_frame, channels='BGR', use_column_width=True)
                st.info(USER_MSG)

            if ideal_frame is not None:
                with col2:
                    start_camera = st.button("Start Camera", key="start")
                    stop_camera = st.button("Stop Camera", key="stop")

                    if start_camera and not stop_camera:
                        self.cap = cv2.VideoCapture(0)
                        time.sleep(1)
                        st_frame = st.empty()

                        while self.cap.isOpened():
                            ret, frame = self.cap.read()
                            if not ret:
                                st.error(CAMERA_NOT_DETECTED_ISSUE)
                                self.cap.release()
                                break

                            frame = cv2.flip(frame, 1)
                            try: 
                                result_img = self.comparison.practice_pose(ideal_frame, frame)
                                st_frame.image(result_img, channels='BGR', use_column_width=True)
                            except:
                                st_frame.error(POSE_NOT_DETECTED_ISSUE)
                            if stop_camera:
                                self.cap.release()
                                break
        except:
            st.error(CAMERA_ISSUE)
    def practice(self):
        st.title(PRACTICE_TITLE)
        practice_option = st.radio('Choose input option:', ["Upload Image", "Live Camera"])

        if practice_option == "Upload Image":
            self.practice_by_image()
        else:
            self.practice_by_feed()