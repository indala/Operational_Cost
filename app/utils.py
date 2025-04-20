import pickle
import os

def load_model():
    model_path = os.path.join("model", "lgbm_model.pkl")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def load_encoder():
    encoder_path = os.path.join("model", "label_encoder.pkl")
    with open(encoder_path, 'rb') as f:
        encoder = pickle.load(f)
    return encoder