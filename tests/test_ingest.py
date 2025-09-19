import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pandas as pd
from ingest import ingest_csv

def test_ingest_csv(tmp_path):
    # Create a sample CSV
    csv_path = tmp_path / "sample.csv"
    df = pd.DataFrame({"id": [1, 2], "value": [10, 20]})
    df.to_csv(csv_path, index=False)
    # Test ingest_csv
    new_rows = ingest_csv(str(csv_path))
    assert len(new_rows) == 2
    assert "id" in new_rows.columns
    assert "value" in new_rows.columns
