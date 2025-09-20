import pandas as pd
from src.quality import check_quality

if __name__ == "__main__":
    # Change this path to a local CSV file for testing
    test_path = "data/sample.csv"
    try:
        check_quality(test_path)
        print("Local test passed.")
    except Exception as e:
        print(f"Local test failed: {e}")
