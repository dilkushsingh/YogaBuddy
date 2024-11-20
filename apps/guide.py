import json
import streamlit as st
from constant import GUIDE_TITLE, SUN_SALUTATION_PARA, NUM_COLS, POSES_FILE_ISSUE

class PoseGuide:
    def __init__(self, data_path, s3utils):
        self.data_path = data_path
        self.s3utils = s3utils
        self.pose_data = self.load_pose_data()

    def load_pose_data(self):
        try:
            json_stream = self.s3utils.fetch_file_content(self.data_path)
            json_data = self.s3utils.stream_to_json(json_stream)
            if json_data is not None:
                return json_data
        except:
            st.error(POSES_FILE_ISSUE)
        return None

    def display_pose(self, pose):
        st.subheader(f"{pose['english_name']} ({pose['hindi_name']})")
        image = self.s3utils.fetch_image(pose['image'])
        if image is not None:
            st.image(image, caption=pose['english_name'], use_column_width=True)
        st.write(pose['description'])

    def display_guide(self):
        st.title(GUIDE_TITLE)
        st.write(SUN_SALUTATION_PARA)
        num_cols = NUM_COLS
        cols = st.columns(num_cols)
        for index, pose in enumerate(self.pose_data.get('poses', [])):
            with cols[index%num_cols]:
                self.display_pose(pose)