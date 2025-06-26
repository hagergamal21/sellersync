# price_suggestion/train_model.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

def train_price_model():
    # Load dataset
    df = pd.read_csv('synthetic_hm_sales_dataset_updated.csv')

    # Preprocessing
    df = df.dropna()

    label_encoder = LabelEncoder()
    df['Sub-Category'] = label_encoder.fit_transform(df['Sub-Category'])

    features = ['Sub-Category', 'Price']  # Adjust based on your real columns
    target = 'Sales Volume'  # Adjust based on your real target column

    X = df[features]
    y = df[target]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train model
    model = LinearRegression()
    model.fit(X_scaled, y)

    # Save model and scaler
    os.makedirs('price_suggestion/models', exist_ok=True)
    joblib.dump(model, 'price_suggestion/models/price_model.pkl')
    joblib.dump(scaler, 'price_suggestion/models/scaler.pkl')
    joblib.dump(label_encoder, 'price_suggestion/models/label_encoder.pkl')

    print("✅ Model, scaler, and label encoder saved successfully.")

if __name__ == "__main__":
    train_price_model()
