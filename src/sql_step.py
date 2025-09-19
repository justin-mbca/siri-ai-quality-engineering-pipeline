import pandas as pd

def run_sql_query(csv_path):
    df = pd.read_csv(csv_path)
    # Example SQL-like query: select rows where value > 100
    result = df.query('value > 100')
    print(f"SQL Query Result:\n{result}")
    # Save result for downstream steps
    result.to_csv(csv_path.replace('.csv', '_sql_result.csv'), index=False)
    return result
