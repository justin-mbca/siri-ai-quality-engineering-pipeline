
from great_expectations.dataset import PandasDataset
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
    ds = PandasDataset(df)
    try:
        assert ds.expect_column_values_to_not_be_null('id')['success']
        assert ds.expect_column_values_to_be_between('value', 0, 1000)['success']
        print('Data quality checks passed.')
    except AssertionError as e:
        print('Data quality check failed.')
        send_alert(
            subject="Data Quality Alert",
            body=f"Data quality check failed for {path}: {str(e)}",
            to_email="recipient@example.com"
        )
        raise

if __name__ == "__main__":
    check_quality('/Users/justin/siri-ai-quality-engineering/data/sample.csv')
