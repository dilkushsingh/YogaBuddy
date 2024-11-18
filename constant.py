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
DISTANCE_THRESHOLD = 0.15

MODEL_PATH = 'models/xgboost_classifier.pkl'
KERAS_MODEL_PATH = 'models/Images_CNN_model.keras'