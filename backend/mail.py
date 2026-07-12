import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_address, subject, message):
    # Standard Flask/SMTP configuration (can be configured via environment variables)
    smtp_server = "localhost"
    smtp_port = 1025  # standard mailhog/development port
    sender_email = "noreply@trekmate.com"
    
    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_address

    # Record the HTML MIME body
    part = MIMEText(message, 'html')
    msg.attach(part)

    try:
        # Try to connect to local SMTP server (e.g. MailHog, python -m smtpd -n -c DebuggingServer localhost:1025)
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.sendmail(sender_email, to_address, msg.as_string())
        server.quit()
        print(f"Email successfully sent to {to_address}")
    except Exception as e:
        print(f"Could not connect to SMTP server: {e}")
        # Print fallback to console for development/debug
        print(f"----- MOCK EMAIL SENT -----")
        print(f"To: {to_address}")
        print(f"Subject: {subject}")
        print(f"Content:\n{message}")
        print(f"---------------------------")
