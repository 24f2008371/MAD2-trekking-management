import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_address, subject, message):
    smtp_server = "localhost"
    smtp_port = 1025
    sender_email = "noreply@trekmate.com"
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_address

    part = MIMEText(message, 'html')
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.sendmail(sender_email, to_address, msg.as_string())
        server.quit()
        print(f"Email successfully sent to {to_address}")
    except Exception as e:
        print(f"Could not connect to SMTP server: {e}")
        print(f"----- MOCK EMAIL SENT -----")
        print(f"To: {to_address}")
        print(f"Subject: {subject}")
        print(f"Content:\n{message}")
        print(f"---------------------------")
