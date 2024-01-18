import base64
from email.message import EmailMessage

from googleapiclient.discovery import build
from config._credentials import GMAIL_API_CREDENTIALS
from email.mime.text import MIMEText
from requests import HTTPError


def gmail_send_message(subject, body, to):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id
    """
  
    service = build("gmail", "v1", credentials=GMAIL_API_CREDENTIALS)
    
    message = MIMEText(body)
    message['subject'] = subject
    message['to'] = to

    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None

