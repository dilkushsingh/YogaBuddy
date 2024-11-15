import json
import streamlit as st
from apps.classify import main as classify
from apps.practice import main as practice
from constant import POSES_DATA_PATH

st.set_page_config(page_title="YogaBuddy", layout="wide")

with open(POSES_DATA_PATH, 'r') as file:
    pose_data = json.load(file)

page = st.sidebar.radio("Choose a page:", ["Guide", "Classify", "Practice"])

def guide():
    st.title("Sun Salutation Guide")
    st.write("""
            The Sun Salutation (Surya Namaskar) is a sequence of yoga poses that warms up the body, 
            stretches the muscles, and increases blood circulation. It is often practiced at the beginning 
            of a yoga session to energize the body and mind. In this guide, you will find detailed instructions 
            for each pose in the Sun Salutation sequence, accompanied by images for better understanding.
        """)    
    cols = st.columns(3)
    for index, pose in enumerate(pose_data['poses']):
        with cols[index % 3]:
            st.subheader(f"{pose['english_name']} ({pose['hindi_name']})")
            st.image(pose['image'], caption=pose['english_name'], use_column_width=True)
            st.write(pose['description'])

if page == "Guide":
    guide()    

elif page == "Classify":
    classify()
    
else:
    practice()    