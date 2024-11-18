import numpy as np
import cv2
import streamlit as st
import time
from constant import IDEAL_POSE_PATH
from utils.practice_pose_utils import process_frames, compare_poses, draw_feedback_on_frame
from utils.streamlit_helpers import fetch_image
   
def fetch_ideal_pose():
    ideal_poses = list(IDEAL_POSE_PATH.keys())
    selected_pose = st.selectbox('Select an Ideal Pose', ideal_poses)
    ideal_pose = cv2.imread(IDEAL_POSE_PATH[selected_pose])
    return ideal_pose

@st.cache_data
def compare_pose(ideal_frame, user_frame):
    ideal_keypoints, ideal_angles = process_frames(ideal_frame)
    user_keypoints, user_angles = process_frames(user_frame)
    feedback = compare_poses(ideal_angles, user_angles)
    result_frame = draw_feedback_on_frame(user_frame, feedback, user_keypoints)
    return result_frame

def practice_by_image():
    try:
        col1, col2 = st.columns(2)
        with col1:
            ideal_frame = fetch_ideal_pose()
            st.image(ideal_frame, channels='BGR', use_column_width=True)
            st.info('Refer to the image above: the red points indicate incorrect angles, while the green points represent correct angles.')

        user_frame = None
        with col2:
            user_frame = fetch_image()
            if ideal_frame is not None and user_frame is not None:
                compare = st.button('Compare Pose')
                if compare:
                    result_img = compare_pose(ideal_frame, user_frame)
                    with col2:
                        st.image(result_img, channels='BGR', use_column_width=True)
    except:
        with col2:
            st.error('There is some issue with uploaded image. Please upload another one.')

def practice_by_feed():
    col1, col2 = st.columns(2)

    with col1:
        ideal_frame = fetch_ideal_pose()
        st.image(ideal_frame, channels='BGR', use_column_width=True)
        st.info('Refer to the image above: the red points indicate incorrect angles, while the green points represent correct angles.')

    if ideal_frame is not None:
        with col2:
            start_camera = st.button("Start Camera", key="start")
            stop_camera = st.button("Stop Camera", key="stop")

            if start_camera and not stop_camera:
                cap = cv2.VideoCapture(0)
                time.sleep(1)
                st_frame = st.empty()
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        st.error('Camera not detected.')
                        cap.release()
                        break

                    frame = cv2.flip(frame, 1)
                    result_img = compare_pose(ideal_frame, frame)
                    st_frame.image(result_img, channels='BGR', use_column_width=True)

                    if stop_camera:
                        cap.release()
                        break

def main():
    st.title('Practice Your Pose')

    practice_option = st.radio('Choose input option:', ["Upload Image", "Live Camera"])

    if practice_option == "Upload Image":
        practice_by_image()

    else:
        practice_by_feed()