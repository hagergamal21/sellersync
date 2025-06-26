import os
import json
import pandas as pd
from prophet import Prophet
from prophet.serialize import model_to_json

# Load and preprocess the dataset
data_path = 'synthetic_hm_sales_dataset_updated.csv'  # Adjust path as needed
df = pd.read_csv(data_path)

# Group and preprocess
grouped_df = (
    df.groupby(['Sub-Category', 'Date', 'semantic_label'])
    .agg(total_quantity=('Quantity', 'sum'))
    .reset_index()
)
grouped_df['Date'] = pd.to_datetime(grouped_df['Date'])
grouped_df['day_of_week'] = grouped_df['Date'].dt.dayofweek
grouped_df['month'] = grouped_df['Date'].dt.month
grouped_df['is_weekend'] = grouped_df['day_of_week'].isin([5, 6]).astype(int)

# Directory to save models
output_dir = 'demand_forecasting/models/'
os.makedirs(output_dir, exist_ok=True)

# Train and save models for each Sub-Category and semantic_label
for (subcategory, semantic_label), group in grouped_df.groupby(['Sub-Category', 'semantic_label']):
    # Prepare data for Prophet
    prophet_df = group[['Date', 'total_quantity']].rename(columns={'Date': 'ds', 'total_quantity': 'y'})
    
    # Train Prophet model
    model = Prophet(daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=True)
    model.fit(prophet_df)
    
    # Save model
    model_filename = f"{subcategory.lower().replace(' ', '_')}_{semantic_label.lower()}.json"
    model_path = os.path.join(output_dir, model_filename)
    with open(model_path, 'w') as f:
        f.write(model_to_json(model))
    print(f"Saved model: {model_path}")

# Save a list of valid Sub-Category and semantic_label combinations
model_index = grouped_df[['Sub-Category', 'semantic_label']].drop_duplicates().to_dict('records')
with open(os.path.join(output_dir, 'model_index.json'), 'w') as f:
    json.dump(model_index, f)