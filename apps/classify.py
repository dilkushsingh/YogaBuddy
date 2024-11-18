import numpy as np
import cv2
import streamlit as st
from utils.pose_classification_xgboost import classify_pose
from utils.streamlit_helpers import fetch_image

def classify_by_image():
    try:
        frame = fetch_image()
        if frame is not None:
            detect = st.button('Detect Pose')
            if detect:
                pose_name = classify_pose(frame)[0]
                st.write('Your current pose is:')
                st.success(pose_name)
                st.image(frame, channels="BGR")
    except:
        st.error('There is some issue with image. Please upload another one.')

def classify_by_feed():
    try:
        start_camera = st.button("Start Camera", key="start")
        stop_camera = st.button("Stop Camera", key="stop")

        if start_camera and not stop_camera:
            cap = cv2.VideoCapture(0)
            status = st.empty()
            pose_placeholder = st.empty()
            st_frame = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.write("Camera not detected.")
                    break
                frame = cv2.flip(frame, 1)
                try:
                    pose_name = classify_pose(frame)[0]
                    status.write('Your current pose is:')
                    pose_placeholder.success(pose_name)
                except:
                    status.error('Pose is not detected. There is some issue with camera.')
                    pose_placeholder.empty()            
                st_frame.image(frame, channels="BGR")

                if stop_camera:
                    cap.release()
                    break
    except:
        st.error('There is some issue with camera.')


def classify():
    st.title("Classify your pose")
    classify_option = st.radio("Choose input method:", ["Upload Image", "Live Camera"])

    if classify_option == "Upload Image":
        classify_by_image()        

    elif classify_option == "Live Camera":
        classify_by_feed()        