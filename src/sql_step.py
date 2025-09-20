import pandas as pd

def run_sql_query(csv_path):
    df = pd.read_csv(csv_path)
    # Example analytics: filter failed actions, calculate intent accuracy, latency stats
    failed_actions = df[df['action_success'] == False]
    print(f"Failed Actions:\n{failed_actions}")
    # Intent accuracy per locale
    if 'parsed_intent' in df.columns and 'locale' in df.columns and 'action_success' in df.columns:
        intent_accuracy = df.groupby(['locale', 'parsed_intent'])['action_success'].mean().reset_index()
        print(f"Intent Accuracy by Locale:\n{intent_accuracy}")
    # Latency stats
    if 'response_time_ms' in df.columns:
        latency_stats = df['response_time_ms'].describe()
        print(f"Latency Stats:\n{latency_stats}")
    # Save failed actions for downstream steps
    failed_actions.to_csv(csv_path.replace('.csv', '_failed_actions.csv'), index=False)
    return failed_actions
