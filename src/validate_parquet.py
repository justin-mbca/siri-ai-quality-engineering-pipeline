import great_expectations as ge
import pandas as pd
import pyarrow.parquet as pq
import glob

# Validate all Parquet files in the output directory
def validate_parquet_files():
    files = glob.glob('data/stream_output/*.parquet')
    for f in files:
        df = pd.read_parquet(f)
        gdf = ge.from_pandas(df)
        # Example expectations
        results = gdf.expect_table_row_count_to_be_between(min_value=1, max_value=100000)
        results &= gdf.expect_column_values_to_not_be_null('value')
        results &= gdf.expect_column_values_to_be_in_set('count', set(range(0, 10000)))
        print(f'Validation results for {f}:', results)

if __name__ == "__main__":
    validate_parquet_files()
