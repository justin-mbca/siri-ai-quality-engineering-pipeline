
# import great_expectations as ge  # No longer used
import pandas as pd
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, body, to_email):
    from_email = 'your_email@example.com'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        with smtplib.SMTP('localhost') as server:
            server.sendmail(from_email, [to_email], msg.as_string())
        print(f"Alert sent to {to_email}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def check_quality(path):
    df = pd.read_csv(path)
    # Fallback: Use pandas for basic data quality checks
    try:
        # Check 1: No missing IDs
        result1 = df['id'].notnull().all()
        # Check 2: 'value' column within range
        result2 = df['value'].between(0, 1000).all()
        # Check 3: No duplicate IDs
        result3 = df['id'].is_unique
        # Check 4: No missing values in any column
        result4 = df.notnull().all().all()
        # Check 5: Outlier detection in 'value' column (z-score > 3)
        if 'value' in df.columns and df['value'].dtype in ['float64', 'int64']:
            z_scores = ((df['value'] - df['value'].mean()) / df['value'].std()).abs()
            result5 = (z_scores < 3).all()
        else:
            result5 = True
        # Aggregate results
        if all([result1, result2, result3, result4, result5]):
            print('Data quality checks passed.')
        else:
            failed_checks = []
            if not result1:
                failed_checks.append('Missing IDs')
            if not result2:
                failed_checks.append('Value out of range')
            if not result3:
                failed_checks.append('Duplicate IDs')
            if not result4:
                failed_checks.append('Missing values in columns')
            if not result5:
                failed_checks.append('Outliers in value column')
            raise AssertionError(f"Data quality check failed: {', '.join(failed_checks)}")
    except Exception as e:
        import traceback
        print('Data quality check failed.')
        print('Exception:', str(e))
        print('Traceback:', traceback.format_exc())
        send_alert(
            subject="Data Quality Alert",
            body=f"Data quality check failed for {path}: {str(e)}\nTraceback: {traceback.format_exc()}",
            to_email="recipient@example.com"
        )
        raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = './data/sample.csv'
    check_quality(csv_path)
