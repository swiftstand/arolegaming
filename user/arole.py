from __future__ import print_function

import os.path

# for authentication
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# for both
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# for email 
import base64
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




def generate_content(customer_name, reset_link):
    text = f"""\
    Hi {customer_name},
    we are sorry to hear that you're having trouble with logging in to Arole Gamers App.
    We've received a message that you've forgotten your password. If this was you, you can get straight back into your account or reset your password now
    {reset_link}
    If you didn't request a password reset, you can ignore this message and learn more about why you might have received it.
    Only people who know your Arole Gamer App password or click the reset your password link in this email can log in to your account."""


    html = """\
    <!DOCTYPE html>
    <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
        <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="x-apple-disable-message-reformatting">
    <!--[if !mso]><!-->
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <!--<![endif]-->
    <title></title>
        <!--[if mso]>
        <style type="text/css">
        table {border-collapse:collapse;border:0;border-spacing:0;margin:0;}
        div, td {padding:0;}
        div {margin:0 !important;}
        </style>
    <noscript>
        <xml>
        <o:OfficeDocumentSettings>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
    <style type="text/css">
        @import url('https://fonts.googleapis.com/css2?family=Poppins');
        @media screen and (max-width: 350px) {
        .three-col .column {
            max-width: 100% !important;
        }
        }
        @media screen and (min-width: 351px) and (max-width: 460px) {
        .three-col .column {
            max-width: 50% !important;
        }
        }
        @media screen and (max-width: 460px) {
        .two-col .column {
            max-width: 100% !important;
        }
        .two-col img {
            width: 100% !important;
        }
        }
        @media screen and (min-width: 461px) {
        .three-col .column {
            max-width: 33.3% !important;
        }
        .two-col .column {
            max-width: 50% !important;
        }
        .sidebar .small {
            max-width: 16% !important;
        }
        .sidebar .large {
            max-width: 84% !important;
        }
        }
    </style>
    </head>
    <body style="margin:0;padding:0;word-spacing:normal;background-color:#ffffff;">
    <div role="article" aria-roledescription="email" lang="en" style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;background-color:#ffffff;">
        <table role="presentation" style="width:100%;border:0;border-spacing:0;">
        <tr>
            <td align="center">
            <!--[if mso]>
            <table role="presentation" align="center" style="width:660px;">
            <tr>
            <td style="padding:20px 0;">
            <![endif]-->
            <div class="outer" style="width:96%;max-width:660px;margin:20px auto;">
                
                <table role="presentation" style="width:100%;border:0;border-spacing:0;">
                <tr>
                    <td style="padding:10px;text-align:left;">
                    <br>""" + """<p style="margin:0;line-height:22px;color: #565a5c;font-size: 13px;font-family: 'Poppins';">Hi {},<br><br>We are sorry to hear that you're having trouble with logging in to Arole gamers App. We've received a message that you've forgotten your password. If this was you, you can get straight back into your account or reset your password now with the code below.</p>""".format(customer_name) + """</td>
                </tr>
                </table>

                <div class="spacer" style="line-height:26px;height:26px;mso-line-height-rule:exactly;">&nbsp;</div>

                <div class="two-col" style="text-align:center;font-size:0;">
                <!--[if mso]>
                <table role="presentation" width="100%">
                <tr>
                <td style="width:50%;padding:10px;" valign="middle">
                <![endif]-->
                <!--[if mso]>
                </td>
                <td style="width:50%;padding:10px;" valign="middle">
                <![endif]-->
                <div class="column" style="width:100%;max-width:330px;display:inline-block;vertical-align:middle;">
                    <div style="padding:10px;font-size:16px;line-height:18px;text-align:center;">""" + """<p style="margin:0;"><a href="" style="background: #ffffff; border-radius: 2px; text-decoration: none; padding: 10px 25px; color: #000000; border-radius: 4px; display:inline-block; mso-padding-alt:0;text-underline-color:#000000"><!--[if mso]><i style="letter-spacing: 25px;mso-font-width:-100%;mso-text-raise:20pt">&nbsp;</i><![endif]--><span style="mso-text-raise:10pt;">{}</span><!--[if mso]><i style="letter-spacing: 25px;mso-font-width:-100%">&nbsp;</i><![endif]--></a></p>""".format(reset_link) + """</div>
                </div>
                <!--[if mso]>
                </td>
                </tr>
                </table>
                <![endif]-->
                </div>

                <div class="spacer" style="line-height:24px;height:24px;mso-line-height-rule:exactly;">&nbsp;</div>

                <table role="presentation" style="width:100%;border:0;border-spacing:0;">
                <tr>
                    <td style="padding:10px;text-align:left;">
                    <p style="margin:0;line-height:22px;color: #949494;font-size: 12px;font-family: 'Poppins';">If you didn't request a password reset, you can ignore this message and learn more about why you might have received it.</p>
                    <br>
                    <p style="margin:0;line-height:22px;color: #949494;font-size: 12px;font-family: 'Poppins';">Only people who know your Arole Gamer App password or Reset your password using the code in this email can log in to your account.</p>
                    </td>
                </tr>
                </table>

                <div class="two-col" style="text-align:center;font-size:0;direction:rtl;">
                <!--[if mso]>
                <table role="presentation" width="100%" dir="rtl">
                <tr>
                <td style="width:50%;padding:10px;" valign="middle" dir="ltr">
                <![endif]-->
                <!--[if mso]>
                </td>
                <td style="width:50%;padding:10px;" valign="middle" dir="ltr">
                <![endif]-->
                <!--[if mso]>
                </td>
                </tr>
                </table>
                <![endif]-->
                </div>

                <div class="spacer" style="line-height:24px;height:24px;mso-line-height-rule:exactly;">&nbsp;</div>
            </div>
            <!--[if mso]>
            </td>
            </tr>
            </table>
            <![endif]-->
            </td>
        </tr>
        </table>
    </div>
    </body>
    </html>

    """

    return text, html


def gmail_send_mail(sender_email, customer_name, customer_email, reset_link):
    """Create and insert a draft email.
       Print the returned draft's message and id.
       Returns: Draft object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
    """
    print("--------------  AUTHENTICATING ----------------\n\n")
    creds = authenticate()
    print("\n\n--------------  DONE ----------------\n\n")

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        # message = EmailMessage()

        message = MIMEMultipart("alternative")
        message["Subject"] = "Arole Gamer App | Reset your password"
        message["From"] = sender_email
        message["To"] = customer_email


        # generate content for the mail both html and plain format
        message_text, message_html = generate_content(customer_name, reset_link)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(message_text, "plain")
        part2 = MIMEText(message_html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)


        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {'raw': encoded_message}

        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())

        print(F'Message Id: {send_message["id"]}')

        success = True


    except HttpError as error:
        print(F'An error occurred: {error}')
        success = False

    return success


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


def authenticate():
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
            try:
                creds.refresh(Request())
            except:
                print("REGENERATING")
                os.remove("token.json")
                authenticate()
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

    return creds


def send_reset_mail(receiver, code, name):
    sender = "aroleplaystation@gmail.com"
    receiver_email = receiver
    gmail_send_mail(sender_email=sender, customer_name=name, customer_email=receiver_email, reset_link=code)




send_reset_mail("swifthmd@gmail.com", "!23456", "Hammed")