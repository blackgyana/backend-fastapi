import smtplib
from email.message import EmailMessage

from src.config import settings



def send_email(msg_subject: str, msg_to_email: str, msg_content: str):
    # set your email and password
    # please use App Password
    email_address = settings.EMAIL_ADDR
    email_password = settings.EMAIL_PASS

    # create email
    msg = EmailMessage()
    msg['Subject'] = msg_subject
    msg['From'] = email_address
    msg['To'] = msg_to_email
    msg.set_content(msg_content)

    # send email
    try:
        with smtplib.SMTP_SSL(settings.SMTP_DOMAIN, settings.SMTP_PORT) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
    except Exception as ex:
        print(f'Error in email sender: {ex}')
        