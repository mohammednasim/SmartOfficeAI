import smtplib

from email.mime.text import MIMEText
#multipurpose internet mail extensions
from email.mime.multipart import MIMEMultipart

from config import EMAIL_ADDRESS
from config import EMAIL_PASSWORD


def send_email(to_email, subject, message):
    """
    Send an email using Gmail SMTP.
    """

    try:

        email = MIMEMultipart()

        email["From"] = EMAIL_ADDRESS
        email["To"] = to_email
        email["Subject"] = subject

        email.attach(
            MIMEText(message, "plain")
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )
        #TLS

        
        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            to_email,
            email.as_string()
        )

        server.quit()

        return "Email sent successfully."

    except Exception as e:

        return f"Email Error: {str(e)}"