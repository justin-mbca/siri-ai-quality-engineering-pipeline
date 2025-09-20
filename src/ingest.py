import os
import pandas as pd

def ingest_csv(path):
    df = pd.read_csv(path)
    # Simulate incremental load: only process new rows
    state_file = path.replace('.csv', '_state.txt')
    last_count = 0
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            last_count = int(f.read().strip())
    new_rows = df.iloc[last_count:]
    print(f'Ingested {len(new_rows)} new rows from {path}')
    # Update state file
    with open(state_file, 'w') as f:
        f.write(str(len(df)))
    # Generate enhanced data profile report for Siri schema
    report_path = path.replace('.csv', '_profile.txt')
    with open(report_path, 'w') as f:
        f.write('Siri Data Profile Report\n')
        f.write('========================\n')
        f.write(f'Shape: {df.shape}\n')
        f.write(f'Columns: {list(df.columns)}\n')
        f.write('\nMissing Values:\n')
        f.write(str(df.isnull().sum()))
        f.write('\n\nDescribe (numeric):\n')
        f.write(str(df.describe(include=["number"])))
        f.write('\n\nDescribe (object):\n')
        f.write(str(df.describe(include=["object"])))
        # Profile key Siri fields
        f.write('\n\nIntent Distribution:\n')
        if 'parsed_intent' in df.columns:
            f.write(str(df['parsed_intent'].value_counts()))
        f.write('\n\nEntity Distribution:\n')
        if 'parsed_entity' in df.columns:
            f.write(str(df['parsed_entity'].value_counts()))
        f.write('\n\nAction Success Rate:\n')
        if 'action_success' in df.columns:
            success_rate = df['action_success'].mean()
            f.write(f"{success_rate:.2%}\n")
        f.write('\n\nAverage Response Time (ms):\n')
        if 'response_time_ms' in df.columns:
            avg_response = df['response_time_ms'].mean()
            f.write(f"{avg_response:.2f}\n")
    print(f"Siri data profile report saved to {report_path}")
    return new_rows

if __name__ == "__main__":
    ingest_csv('/opt/airflow/data/sample.csv')
