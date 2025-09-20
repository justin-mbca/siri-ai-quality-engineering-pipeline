import pandas as pd
from src.quality import check_quality

def test_quality_pass():
    # All checks should pass
    df = pd.DataFrame({'id': [1, 2, 3], 'value': [100, 200, 300]})
    df.to_csv('test_sample.csv', index=False)
    try:
        check_quality('test_sample.csv')
    except Exception:
        assert False, "Quality check should pass for valid data"

def test_quality_fail_missing_id():
    # Should fail due to missing id
    df = pd.DataFrame({'id': [1, None, 3], 'value': [100, 200, 300]})
    df.to_csv('test_sample.csv', index=False)
    try:
        check_quality('test_sample.csv')
        assert False, "Quality check should fail for missing id"
    except AssertionError:
        pass

def test_quality_fail_outlier():
    # Should fail due to outlier
    df = pd.DataFrame({'id': [1, 2, 3], 'value': [100, 200, 9999]})
    df.to_csv('test_sample.csv', index=False)
    try:
        check_quality('test_sample.csv')
        assert False, "Quality check should fail for outlier"
    except AssertionError:
        pass

if __name__ == "__main__":
    test_quality_pass()
    test_quality_fail_missing_id()
    test_quality_fail_outlier()
    print("All quality tests passed.")
