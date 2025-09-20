
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
    # Siri schema quality checks
    try:
        # Check 1: No missing interaction_id
        result1 = df['interaction_id'].notnull().all() if 'interaction_id' in df.columns else False
        # Check 2: response_time_ms within reasonable range (100-2000 ms)
        result2 = df['response_time_ms'].between(100, 2000).all() if 'response_time_ms' in df.columns else True
        # Check 3: No duplicate interaction_id
        result3 = df['interaction_id'].is_unique if 'interaction_id' in df.columns else True
        # Check 4: No missing values in any column
        result4 = df.notnull().all().all()
        # Check 5: Outlier detection in response_time_ms (z-score > 3)
        if 'response_time_ms' in df.columns and df['response_time_ms'].dtype in ['float64', 'int64']:
            z_scores = ((df['response_time_ms'] - df['response_time_ms'].mean()) / df['response_time_ms'].std()).abs()
            result5 = (z_scores < 3).all()
        else:
            result5 = True
        # Check 6: Action success rate should be > 60%
        if 'action_success' in df.columns:
            success_rate = df['action_success'].mean()
            result6 = success_rate > 0.6
        else:
            result6 = True
        # Aggregate results
        if all([result1, result2, result3, result4, result5, result6]):
            print('Siri data quality checks passed.')
        else:
            failed_checks = []
            if not result1:
                failed_checks.append('Missing interaction_id')
            if not result2:
                failed_checks.append('response_time_ms out of range')
            if not result3:
                failed_checks.append('Duplicate interaction_id')
            if not result4:
                failed_checks.append('Missing values in columns')
            if not result5:
                failed_checks.append('Outliers in response_time_ms')
            if not result6:
                failed_checks.append('Low action success rate')
            raise AssertionError(f"Siri data quality check failed: {', '.join(failed_checks)}")
    except Exception as e:
        import traceback
        print('Siri data quality check failed.')
        print('Exception:', str(e))
        print('Traceback:', traceback.format_exc())
        send_alert(
            subject="Siri Data Quality Alert",
            body=f"Siri data quality check failed for {path}: {str(e)}\nTraceback: {traceback.format_exc()}",
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
