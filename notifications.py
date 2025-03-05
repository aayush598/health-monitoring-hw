import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "your_password"
RECIPIENT_EMAIL = "recipient@example.com"

def send_notification(message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = "Health Alert Notification"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send notification: {e}")