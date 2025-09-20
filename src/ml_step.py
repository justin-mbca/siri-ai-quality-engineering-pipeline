import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def run_ml_pipeline(csv_path):
    df = pd.read_csv(csv_path)
    # Predict response_time_ms from device_type, intent, and repeat_count
    from sklearn.preprocessing import LabelEncoder
    features = []
    if 'device_type' in df.columns:
        le_device = LabelEncoder()
        df['device_type_enc'] = le_device.fit_transform(df['device_type'])
        features.append('device_type_enc')
    if 'parsed_intent' in df.columns:
        le_intent = LabelEncoder()
        df['intent_enc'] = le_intent.fit_transform(df['parsed_intent'])
        features.append('intent_enc')
    if 'repeat_count' in df.columns:
        features.append('repeat_count')
    X = df[features].values if features else df.index.values.reshape(-1, 1)
    y = df['response_time_ms'].values if 'response_time_ms' in df.columns else None
    if y is not None:
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        print(f"Predicted Response Times: {predictions}")
        df['predicted_response_time_ms'] = predictions
        df.to_csv(csv_path.replace('.csv', '_ml_result.csv'), index=False)
        return predictions
    else:
        print("No response_time_ms column found for ML step.")
        return None
