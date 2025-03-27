import smtplib
import json
from email.message import EmailMessage
from src.lib.logger import logger

class EmailClient():
    
    def __init__(self, profile):
        self.profile = profile
        
    def gmail_send_message(self, recipient: str, subject: str, content: str):
        """Send an email using SMTP with Gmail."""
        
        email_message = EmailMessage()
        email_message.set_content(content)
        email_message["To"] = recipient
        email_message["From"] = self.profile.gmail_login
        email_message["Subject"] = subject
        email_message["Bcc"] = self.profile.gmail_login # add myself to be informed

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.profile.gmail_login, self.profile.gmail_password)
                server.send_message(email_message)
        except Exception as error:
                logger.error(f"Error occurred while sending an email: {error}")