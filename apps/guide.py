import json
import streamlit as st
from constant import GUIDE_TITLE, SUN_SALUTATION_PARA, NUM_COLS

class PoseGuide:
    def __init__(self, data_path):
        self.data_path = data_path
        self.pose_data = self.load_pose_data()

    @st.cache_data
    def load_pose_data(self):
        try:
            with open(self.data_path, 'r') as file:
                return json.load(file)
        except:
            st.error('There is some issue with the Poses data file.')

    def display_guide(self):
        st.title(GUIDE_TITLE)
        st.write(SUN_SALUTATION_PARA)
        num_cols = NUM_COLS
        cols = st.columns(num_cols)
        for index, pose in enumerate(self.pose_data['poses']):
            with cols[index%num_cols]:
                self.display_pose(pose)

    @staticmethod
    def display_pose(pose):
        st.subheader(f"{pose['english_name']} ({pose['hindi_name']})")
        st.image(pose['image'], caption=pose['english_name'], use_column_width=True)
        st.write(pose['description'])