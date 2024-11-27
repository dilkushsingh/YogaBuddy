import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report
from constant import TRAIN_DIR, TEST_DIR
import os
import joblib
import argparse

def load_data(dir):
    data = pd.read_csv(dir)
    x_data, y_data = data.iloc[:, :-1], data.iloc[:, -1]
    return x_data, y_data

def preprocess_labels(y_train):
    lab_enc = LabelEncoder()
    y_train_enc = lab_enc.fit_transform(y_train)
    return y_train_enc, lab_enc

def train_model(X_train, y_train_enc, max_depth, objective, n_estimators, learning_rate):
    classifier = xgb.XGBClassifier(
        max_depth=max_depth,
        objective=objective,
        n_estimators=n_estimators,
        learning_rate=learning_rate
    )
    classifier.fit(X_train, y_train_enc)
    return classifier

def evaluate_model(classifier, X_test, y_test, lab_enc):
    y_pred_enc = classifier.predict(X_test)
    y_pred = lab_enc.inverse_transform(y_pred_enc)

    cm = confusion_matrix(y_test, y_pred)
    print('\nConfusion Matrix:\n', cm)
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

def save_model(classifier, output_dir):
    model_path = os.path.join(output_dir, 'xgboost_classifier.pkl')
    with open(model_path, 'wb') as f:
        joblib.dump(classifier, f)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train an XGBoost classifier.")
    parser.add_argument('--output_dir', type=str, default='.', help="Directory to save model and outputs")
    parser.add_argument('--max_depth', type=int, default=5, help="Maximum depth of trees")
    parser.add_argument('--objective', type=str, default='multi:softprob', help='Objective function')
    parser.add_argument('--n_estimators', type=int, default=500, help="Number of estimators")
    parser.add_argument('--learning_rate', type=float, default=0.35, help="Learning rate for boosting")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    X_train, y_train = load_data(TRAIN_DIR)
    X_test, y_test = load_data(TEST_DIR)
    y_train_enc, label_encoder = preprocess_labels(y_train)

    classifier = train_model(X_train, y_train_enc, args.max_depth, args.objective, args.n_estimators, args.learning_rate)

    evaluate_model(classifier, X_test, y_test, label_encoder)

    save_model(classifier, args.output_dir)