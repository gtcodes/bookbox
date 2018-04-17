import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.discovery import build
from apiclient import errors

SCOPES = 'https://www.googleapis.com/auth/gmail.send'

def getCredentials():
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service

# send message
def SendMessage(service, sender, to, subject, msgHtml, msgPlain):
    message = CreateMessageHtml(sender, to, subject, msgHtml, msgPlain)
    try:
        message = (service.users().messages().send(userId="me", body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    return "OK"

# create the message to send
def CreateMessageHtml(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    return {'raw': raw}

service = getCredentials()

to = "joker@gtg.se"
sender = "youremail@gmail.com"
subject = "testmail from python"
msgHtml = "Hi<br/>Html Email"
msgPlain = "Hi\nPlain Email"
SendMessage(service, sender, to, subject, msgHtml, msgPlain)
