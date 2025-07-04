import base64
import os.path
from email.message import EmailMessage
from email.utils import make_msgid

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send_email(address_to: str, message_text: str, image_path: str):
  # If modifying these scopes, delete the file token.json.

  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "Infrastructure/utilities/mail_sending/auth2_gmail_send/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    image_cid = make_msgid(domain="example.com")[1:-1]

    html = f"""
            <html>
              <body>
                <p>{message_text}</p>
                <img src="cid:{image_cid}" alt="QrCode" />
              </body>
            </html>
            """

    message.set_content(message_text)
    message.add_alternative(html, subtype='html')

    # add image
    if os.path.exists(image_path):
      print("Image exists")
    with open(image_path, 'rb') as img:
      img_data = img.read()

    # inline attachment
    message.get_payload()[1].add_related(img_data, maintype='image', subtype='gif', cid=f"<{image_cid}>")

    message["To"] = address_to
    message["From"] = "SchoolCoffeeDummyBoi@gmail.com"
    message["Subject"] = "Test"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
      service.users()
      .messages()
      .send(userId="me", body=create_message)
      .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None


