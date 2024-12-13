import tensorflow as tf
import numpy as np
import io
from ..database import MLModel, SessionLocal

def save_model_to_db(model, name, version="1.0.0"):
    """
    Save TensorFlow model to PostgreSQL
    """
    model_bytes = io.BytesIO()
    tf.keras.models.save_model(model, model_bytes, save_format='h5')
    model_bytes = model_bytes.getvalue()
    
    db = SessionLocal()
    db_model = MLModel(
        name=name,
        version=version,
        model_data=model_bytes
    )
    db.add(db_model)
    db.commit()
    db.close()

def load_model_from_db(name):
    """
    Load TensorFlow model from PostgreSQL
    """
    db = SessionLocal()
    db_model = db.query(MLModel).filter(MLModel.name == name).first()
    if not db_model:
        raise ValueError(f"Model {name} not found in database")
    
    model_bytes = io.BytesIO(db_model.model_data)
    model = tf.keras.models.load_model(model_bytes)
    db.close()
    
    return model

def preprocess_data(data):
    """
    Preprocess input data for model prediction
    Override this function with your specific preprocessing logic
    """
    return np.array(data)
