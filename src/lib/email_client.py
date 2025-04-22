import smtplib
import json
from email.message import EmailMessage
from src.lib.logger import logger
import imaplib
import re

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
    
    def retrieve_6digit_code(self):     
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(self.profile.gmail_login2, self.profile.gmail_password2)
        mail.list()
        mail.select("inbox")  # connect to inbox
        result, data = mail.search(None, "ALL")

        ids = data[0]  # data is a list
        id_list = ids.split()  # ids is a space-separated string

        # Reverse the order of emails
        for email_id in reversed(id_list):
            # fetch the email body (RFC822) for the given ID
            result, data = mail.fetch(email_id, "(RFC822)") 
            raw_email = data[0][1]  # here's the body, which is raw text of the whole email
            matches = re.findall(r'\b\d{6}\b', raw_email.decode('utf-8', errors='ignore'))  # find all 6-digit codes
            if matches:
                logger.info(f"Found {len(matches)} matching groups: {matches}")
                code = matches[-1]  # take the first match
                # Delete the email after retrieving the code
                mail.store(email_id, '+FLAGS', '\\Deleted')
                mail.expunge()
                return code
                
        return "No code found"
