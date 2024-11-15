import numpy as np
import cv2
import streamlit as st

def fetch_image():
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        file_bytes = np.asarray(bytearray(uploaded_image.read()))
        frame = cv2.imdecode(file_bytes, 1)
        if frame is None:
            raise ValueError()
        return frame
    return None