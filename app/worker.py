import tensorflow as tf
from .ml.model import load_model_from_db
from .ml.model import preprocess_data

def predict_async(data):
    """
    Async prediction function for the worker
    """
    model = load_model_from_db("default_model")
    processed_data = preprocess_data(data)
    prediction = model.predict(processed_data)
    return prediction.tolist()
