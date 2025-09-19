import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from transform import transform_data

def test_transform_data():
    # This is a placeholder; add Spark test logic as needed
    assert callable(transform_data)
