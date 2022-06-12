from __future__ import print_function

import os
import time
import sib_api_v3_sdk
from django.conf import settings
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint


# api_key = settings.SENDBLUE_API_KEY
api_key = os.getenv('SENDBLUE_API_KEY')

# Configure API key authorization: api-key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = api_key

# Uncomment below lines to configure API key authorization using: partner-key
# configuration = sib_api_v3_sdk.Configuration()
# configuration.api_key['partner-key'] = 'YOUR_API_KEY'

# create an instance of the API class


def sent_email_now(recipient, message):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[recipient],
        sender={"name": "abhishek fegno", "email": "abhishekfegno@gmail.com"},
        # template_id=2,
        params={"name": recipient.get('name'), "headline": message},  # used to render inside email template
        headers={"X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3",
                 "charset": "iso-8859-1",
                 "api-key": api_key,
                 "content-type": "application/json",
                 "accept": "application/json"
                 },
        # text_content=message,
        subject="Notification to admin !!",
        # html_content=message
    )  # SendSmtpEmail | Values to send a transactional email

    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
        print("<<<<<<email sent>>>>>>")

    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

#


recipient = {"email": "raviabhishek445@gmail.com", "name": "Abhishek Ravi"}
# url = "hairtrix.salon.dev.fegno.com"
# message = f'You have successfullly created your domain name please check {url} to login'
message1 = "test email for maxpolo"
sent_email_now(recipient, message1)
