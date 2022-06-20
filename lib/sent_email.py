from __future__ import print_function

import os
import time
import sib_api_v3_sdk
from django.conf import settings
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint




class EmailHandler(object):
    api_key = os.environ.get('SENDINBLUE_API_KEY')

    # Configure API key authorization: api-key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    # Uncomment below lines to configure API key authorization using: partner-key
    # configuration = sib_api_v3_sdk.Configuration()
    # configuration.api_key['partner-key'] = 'YOUR_API_KEY'

    # create an instance of the API class


    def sent_email_now(self, recipient, message, subject):
        print("KEY", self.api_key)
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[recipient],
            sender={"name": "Fegno Technologies", "email": "abhishekfegno@gmail.com"},
            template_id=3,
            params={"name": recipient.get('name'), "subheadline": subject.get("subheadline"), "message": message},  # used to render inside email template
            headers={"X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3",
                     "charset": "iso-8859-1",
                     "api-key": self.api_key,
                     "content-type": "application/json",
                     "accept": "application/json"
                     },
            # text_content=message,
            subject=subject.get("subject"),
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


# recipient = {"email": "raviabhishek445@gmail.com", "name": "Abhishek Ravi"}
# # absolute uri with username
# url = "URL"
# subject = {
#     "subject": "Password Reset",
#     "subheadline": "You have requested for a Password Reset"
#     }
# message1 = f'You can reset you password by visiting this link {url}'
# e = EmailHandler()
# e.sent_email_now(recipient, message1, subject)


