import smtplib
from email.mime.text import MIMEText

GMAIL_USER = "comsolmultip@gmail.com"
GMAIL_PASSWORD = "mgqb rkhj enke wdsw"

def send_email(to_email: str, subject: str, message: str):
    """Invia un'email di testo semplice"""
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
    except Exception as e:
        print(f"Errore invio email: {e}")