import streamlit as st
from apps.guide import PoseGuide
from apps.classify import PoseClassifier
from apps.practice import PosePractice
from constant import PAGE_TITLE, PAGE_LAYOUT, POSES_DATA_PATH, MODEL_PATH, POSE_CLASSES, ANGLE_THRESHOLD

st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT)

page = st.sidebar.radio("Choose a page:", ["Guide", "Classify", "Practice"])

def guide():
    guide = PoseGuide(POSES_DATA_PATH)
    guide.display_guide()

def classify():
    classify = PoseClassifier(MODEL_PATH, POSE_CLASSES)
    classify.display()
    
def practice():
    practice = PosePractice(ANGLE_THRESHOLD)
    practice.practice()

if page == "Guide":
    guide()    
elif page == "Classify":
    classify() 
else:
    practice()    