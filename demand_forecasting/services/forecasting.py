# demand_forecasting/services/forecasting.py

import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64
import uuid
import joblib
from django.conf import settings

def load_data():
    dataset_path = os.path.join(settings.BASE_DIR, 'models', 'synthetic_hm_sales_dataset_updated.csv')
    df = pd.read_csv(dataset_path)
    return df

def load_model(subcategory, semantic_label):
    model_filename = f"{subcategory}_{semantic_label}.pkl"
    model_path = os.path.join(settings.BASE_DIR, 'models', model_filename)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file {model_filename} not found.")
    
    model = joblib.load(model_path)
    return model

def forecast_demand(subcategory, semantic_label, days_to_predict, current_inventory, base_price):
    model = load_model(subcategory, semantic_label)

    future = model.make_future_dataframe(periods=days_to_predict)
    forecast = model.predict(future)

    forecast_tail = forecast.tail(days_to_predict)

    # Add 'status' column
    forecast_tail = forecast_tail.copy()
    forecast_tail['status'] = forecast_tail['yhat'].apply(
        lambda x: 'Increase' if x > current_inventory else ('Maintain' if abs(x - current_inventory) < 5 else 'Decrease')
    )

    # Generate first plot (Forecast Plot)
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    model.plot(forecast, ax=ax1)
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    plt.close(fig1)
    plot_url_demand = base64.b64encode(buf1.getvalue()).decode('utf-8')
    buf1.close()

    # Generate second plot (Inventory vs Forecast)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(forecast_tail['ds'], forecast_tail['yhat'], label='Forecasted Demand', marker='o')
    ax2.axhline(y=current_inventory, color='red', linestyle='--', label='Current Inventory')
    ax2.set_title('Forecast vs Current Inventory')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Quantity')
    ax2.legend()
    ax2.grid(True)
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    plt.close(fig2)
    plot_url_inventory = base64.b64encode(buf2.getvalue()).decode('utf-8')
    buf2.close()

    # Inventory Calculations
    total_forecasted_demand = forecast_tail['yhat'].sum()
    inventory_shortfall = max(0, total_forecasted_demand - current_inventory)
    inventory_excess = max(0, current_inventory - total_forecasted_demand)
    projected_revenue = total_forecasted_demand * base_price

    inventory_status = {
        'total_forecasted_demand': total_forecasted_demand,
        'current_inventory': current_inventory,
        'inventory_shortfall': inventory_shortfall,
        'inventory_excess': inventory_excess,
    }

    # Return embedded plots (not file paths)
    return forecast_tail.to_dict('records'), plot_url_demand, plot_url_inventory, inventory_status
