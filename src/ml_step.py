import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def run_ml_pipeline(csv_path):
    df = pd.read_csv(csv_path)
    # Simple ML: Predict 'value' from 'id'
    X = df[['id']].values
    y = df['value'].values
    model = LinearRegression()
    model.fit(X, y)
    predictions = model.predict(X)
    print(f"ML Predictions: {predictions}")
    # Save predictions
    df['predicted_value'] = predictions
    df.to_csv(csv_path.replace('.csv', '_ml_result.csv'), index=False)
    return predictions
