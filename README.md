# YogaBuddy - AI Yoga Assistant

YogaBuddy is an AI-powered yoga assistant designed to help users practice Sun Salutation poses effectively. Built using Streamlit, it offers pose guidance, pose classification, and real-time feedback, leveraging image-based and keypoint-based models for accuracy.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Model Overview](#model-overview)
- [Model Details](#model-details)
- [Classification Reports](#classification-reports)
- [Dependencies](#dependencies)
- [Future Enhancements](#future-enhancements)
- [Contributions](#contributions)

## Overview

YogaBuddy is a user-friendly assistant focused on the Sun Salutation (Surya Namaskar) sequence of yoga poses. It offers three main functionalities:

1. **Guide**: Visual and textual guidance for Sun Salutation poses, perfect for beginners.
2. **Classify**: Classifies uploaded or live camera images into specific Sun Salutation poses.
3. **Practice**: Provides angle-based feedback to help users improve their yoga pose alignment.

## Getting Started

1. **Clone the repository**:
    ```bash
    git clone https://github.com/dilkushsingh/YogaBuddy.git
    cd YogaBuddy
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate   # On Windows use: myenv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

5. **If you want to train the model, run the following command**
    ```bash
    python train.py --output_dir ./output --max_depth 5 --objective 'multi:softprob'  --n_estimators 500 --learning_rate 0.35
    ```

## Model Overview

Below is a flowchart diagram of the YogaBuddy system pipeline:

![Model Overview](logs/project_overview.png)

## Model Details

### Classification Models

YogaBuddy integrates multiple models trained on pose data, including:

- **Image-based Neural Network**: Built using TensorFlow, trained on pose images for classification.
- **Keypoint-based Neural Network**: Classifies poses using extracted body keypoints.
- **Keypoint-based KNN**: Identifies poses based on proximity in keypoint feature space (using `sklearn` library).
- **Keypoint-based XGBoost Classifier**: Uses keypoint data with a boosted algorithm for pose classification.

*For the Streamlit app, YogaBuddy uses the XGBoost classifier for real-time and reliable pose classification.*

### Keypoint Detection

MediaPipe is used for real-time keypoint detection, which supports both classification and angle-based feedback. This enables precise evaluation and alignment correction for users practicing poses.

## Classification Reports

Below are the confusion matrices for the four classification models trained on the Sun Salutation dataset:

| ![Image-based Neural Network](reports/image_cnn_confusion_matrix.png) | ![Keypoint-based Neural Network](reports/keypoints_nn_confusion_matrix.png) |
| --- | --- |
| **Image-based Neural Network** | **Keypoint-based Neural Network** |

| ![Keypoint-based KNN Classifier](reports/keypoints_knnc_confusion_matrix.png) | ![Keypoint-based XGBoost Classifier](reports/keypoints_xgb_confusion_matrix.png) |
| --- | --- |
| **Keypoint-based KNN Classifier** | **Keypoint-based XGBoost Classifier** |

These confusion matrices provide insight into the models performance across the seven Sun Salutation poses.

## Dependencies

- **Streamlit** - App interface development.
- **OpenCV** - Image and video processing.
- **MediaPipe** - Keypoint detection.
- **TensorFlow** - For training image-based models.
- **XGBoost** - For real-time pose classification in the app.
- **scikit-learn** - For KNN-based pose classification.
- Refer to `requirements.txt` for the complete list of dependencies.

## Future Enhancements

- Integrate a fine-tuned large language model (LLM) to provide additional yoga-related knowledge and insights.
- Add voice-based real-time instructions for pose correction.
- Include advanced yoga poses and sequences.
- Develop detailed body-part-specific error analysis during practice.

## Contributions

Contributions are welcome to make YogaBuddy more robust and versatile.
We encourage contributions in the following areas:
- Adding advanced yoga poses or sequences.
- Improving pose correction accuracy.
- Enhancing the user interface for better engagement.
