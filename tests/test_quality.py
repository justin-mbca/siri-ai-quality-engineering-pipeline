import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pandas as pd
from quality import check_quality

def test_check_quality(tmp_path):
    csv_path = tmp_path / "sample.csv"
    df = pd.DataFrame({"id": [1, 2], "value": [100, 200]})
    df.to_csv(csv_path, index=False)
    # Should not raise
    check_quality(str(csv_path))
