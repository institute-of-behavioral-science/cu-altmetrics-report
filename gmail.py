"""from https://developers.google.com/gmail/api/guides/sending#python
This Module allows sending email through Gmail"""

from __future__ import print_function
import base64
import os
from email.message import EmailMessage
from mimetypes import guess_type

from urllib.error import HTTPError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_emails(emails, dev_emails=None):
    """Determines what environment we're running in and then sets emails accordingly"""
    if bool(os.environ.get('DEV', False)) and dev_emails is not None:
        return dev_emails
    return emails

def setup():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message_with_attachment(
        email_from, email_to, email_subject, email_body, email_attachment=None):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.
      file: The path to the file to be attached.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = EmailMessage()
    message['From'] = email_from
    message['To'] = email_to
    message['Subject'] = email_subject
    message.add_alternative(email_body, subtype='html')
    if email_attachment:
        mime_type, _ = guess_type(email_attachment)
        mime_type, mime_subtype = mime_type.split('/', 1)
        with open(email_attachment, 'rb') as ap:
            message.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, filename=os.path.basename(email_attachment))

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(f"Message Id: { message['id'] }")
        return message
    except HTTPError as error:
        print(f"An error occurred: { error }")
