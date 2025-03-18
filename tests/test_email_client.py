from lib.email_client import EmailClient

email_client = EmailClient()

email_client.gmail_send_message(
    "tesnarmm@gmail.com",
    "Test",
    "test"
)