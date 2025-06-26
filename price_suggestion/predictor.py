# price_suggestion/predictor.py

import joblib
import numpy as np
import os

# Load the model, scaler, and label encoder once when the app starts
model_path = os.path.join('price_suggestion', 'models', 'price_model.pkl')
scaler_path = os.path.join('price_suggestion', 'models', 'scaler.pkl')
label_encoder_path = os.path.join('price_suggestion', 'models', 'label_encoder.pkl')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
label_encoder = joblib.load(label_encoder_path)

def predict_sales(sub_category: str, price: float) -> float:
    """
    Predict sales based on sub-category and price.
    """
    # Encode sub-category
    sub_category_encoded = label_encoder.transform([sub_category])[0]

    # Create feature array
    features = np.array([[sub_category_encoded, price]])

    # Scale features
    features_scaled = scaler.transform(features)

    # Predict
    sales_prediction = model.predict(features_scaled)

    return sales_prediction[0]
