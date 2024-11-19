# app.py
PAGE_TITLE = "YogaBuddy"
PAGE_LAYOUT = "wide"

# apps/guide.py
POSES_DATA_PATH = 'data/poses_data.json'
GUIDE_TITLE = "Sun Salutation Guide"
SUN_SALUTATION_PARA = """
The Sun Salutation (Surya Namaskar) is a sequence of yoga poses that warms up the body, 
stretches the muscles, and increases blood circulation. It is often practiced at the beginning 
of a yoga session to energize the body and mind. In this guide, you will find detailed instructions 
for each pose in the Sun Salutation sequence, accompanied by images for better understanding.
"""
NUM_COLS = 3

# apps/classify.py
CLASSIFY_TITLE = "Classify your pose"
POSE_CLASSES = ['Ashtanga Namaskara', 'Ashwa Sanchalanasana', 'Bhujangasana', 'Hasta Uttanasana', 'Parvatasana', 'Pranamasana', 'Uttanasana']
MODEL_PATH = 'models/xgboost_classifier.pkl'

# issues
POSES_FILE_ISSUE = "There is some issue with the Poses data file."
UPLOAD_ISSUE = "There is some issue with the image. Please upload another one."
POSE_NOT_DETECTED_ISSUE = "Pose not detected. There is some issue with the camera."
CAMERA_ISSUE = "There is some issue with the camera."
CAMERA_NOT_DETECTED_ISSUE = "Camera not detected."

# apps/practice.py
PRACTICE_TITLE = "Practice Your Pose"
USER_MSG = "Refer to the image above: the red points indicate incorrect angles, while the green points represent correct angles."
IDEAL_POSE_PATH = {
    "Pranamasana": "data/sun_salutation_poses/ideals/Pranamasana.jpg",
    "Hasta Uttanasana": "data/sun_salutation_poses/ideals/HastaUttanasana.jpg",
    "Uttanasana": "data/sun_salutation_poses/ideals/Uttanasana.jpg",
    "Ashwa Sanchalanasana": "data/sun_salutation_poses/ideals/AshwaSanchalasana.jpg",
    "Parvatasana": "data/sun_salutation_poses/ideals/Parvatasana.jpg",
    "Ashtanga Namaskara": "data/sun_salutation_poses/ideals/AshtangaNamaskara.jpg",
    "Bhujangasana": "data/sun_salutation_poses/ideals/Bhujangasana.jpg"
}
ANGLE_THRESHOLD = 5

# train.py
TRAIN_DIR = 'data/train.csv'
TEST_DIR = 'data/test.csv'