import streamlit as st
from apps.guide import PoseGuide
from apps.classify import classify
from apps.practice import practice
from constant import PAGE_TITLE, PAGE_LAYOUT, POSES_DATA_PATH

st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT)

page = st.sidebar.radio("Choose a page:", ["Guide", "Classify", "Practice"])

def guide():
    guide = PoseGuide(POSES_DATA_PATH)
    guide.display_guide()

if page == "Guide":
    guide()    
elif page == "Classify":
    classify() 
else:
    practice()    