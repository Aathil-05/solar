import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAIN_MODEL = joblib.load(os.path.join(BASE_DIR, "rain_model.pkl"))
LABEL_ENCODER = joblib.load(os.path.join(BASE_DIR, "label_encoder.pkl"))
FEATURE_ORDER = joblib.load(os.path.join(BASE_DIR, "feature_order.pkl"))
