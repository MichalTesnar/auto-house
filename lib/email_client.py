import smtplib
import json
from email.message import EmailMessage
from lib.logger import logger

class EmailClient():
    
    def __init__(self):
        with open('secret/gmail_credentials.json') as f:
            data = json.load(f)
            self.login = data["login"]
            self.password = data["password"]

    def gmail_send_message(self, recipient: str, subject: str, content: str):
        """Send an email using SMTP with Gmail."""
        
        email_message = EmailMessage()
        email_message.set_content(content)
        email_message["To"] = recipient
        email_message["From"] = self.login
        email_message["Subject"] = subject

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.login, self.password)
                server.send_message(email_message)
        except Exception as error:
                logger.error(f"Error occurred while sending an email: {error}")