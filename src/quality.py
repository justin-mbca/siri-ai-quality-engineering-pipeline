
import great_expectations as ge
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
    gdf = ge.from_pandas(df)
    try:
        result1 = gdf.expect_column_values_to_not_be_null('id')
        result2 = gdf.expect_column_values_to_be_between('value', min_value=0, max_value=1000)
        if result1["success"] and result2["success"]:
            print('Data quality checks passed.')
        else:
            raise AssertionError('Data quality check failed.')
    except AssertionError as e:
        print('Data quality check failed.')
        send_alert(
            subject="Data Quality Alert",
            body=f"Data quality check failed for {path}: {str(e)}",
            to_email="recipient@example.com"
        )
        raise

if __name__ == "__main__":
    check_quality('/opt/airflow/data/sample.csv')
