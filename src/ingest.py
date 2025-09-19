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
    # Generate simple data profile report
    report_path = path.replace('.csv', '_profile.txt')
    with open(report_path, 'w') as f:
        f.write('Data Profile Report\n')
        f.write('===================\n')
        f.write(f'Shape: {df.shape}\n')
        f.write(f'Columns: {list(df.columns)}\n')
        f.write('\nMissing Values:\n')
        f.write(str(df.isnull().sum()))
        f.write('\n\nDescribe:\n')
        f.write(str(df.describe(include="all")))
    print(f"Data profile report saved to {report_path}")
    return new_rows

if __name__ == "__main__":
    ingest_csv('/Users/justin/siri-ai-quality-engineering/data/sample.csv')
