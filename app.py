import streamlit as st
from apps import PoseGuide, PoseClassifier, PosePractice
from utils.data_utils import S3Utils
from constant import PAGE_TITLE, PAGE_LAYOUT, POSES_DATA_PATH, MODEL_PATH, POSE_CLASSES, ANGLE_THRESHOLD
from constant import AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME, BUCKET_NAME

st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT)

page = st.sidebar.radio("Choose a page:", ["Guide", "Classify", "Practice"])

s3utils = S3Utils(AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME, BUCKET_NAME)

@st.cache_data
def guide():
    guide = PoseGuide(POSES_DATA_PATH, s3utils)
    guide.display_guide()

def classify():
    classify = PoseClassifier(MODEL_PATH, POSE_CLASSES)
    classify.display()
 
def practice():
    practice = PosePractice(ANGLE_THRESHOLD, s3utils)
    practice.practice()

if page == "Guide":
    guide()    
elif page == "Classify":
    classify() 
else:
    practice()    