from __future__ import print_function

import os
from pprint import pprint

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# from apps.user.models import Dealer
from lib.events import EventHandler


class EmailHandler(EventHandler):
    api_key = os.environ.get('SENDINBLUE_API_KEY')
    # print(api_key)
    # Configure API key authorization: api-key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    # Uncomment below lines to configure API key authorization using: partner-key
    # configuration = sib_api_v3_sdk.Configuration()
    # configuration.api_key['partner-key'] = 'YOUR_API_KEY'

    # create an instance of the API class

    def event_for_pdfs(self, recipients, instance):
        from apps.user.models import User
        admins = User.objects.filter(is_superuser=True)
        url = ""
        from apps.user.models import Dealer

        recipient = [i for i in Dealer.objects.all().values('email', 'first_name')]
        for admin in admins:
            recipient.append({'email': 'admin@gmail.com', 'first_name': 'admin'})
        message = f"New products have been arrived.Please visit {url}"
        subject = {
            "subject": "New Product",
            "subheadline": "New products have been arrived !!!"
            }
        self.sent_email_now(recipient, message, subject)


    def event_for_banners(self, recipients, instance):
        from apps.user.models import User
        admins = User.objects.filter(is_superuser=True)
        url = ""
        for admin in admins:
            recipients.append({'email': admin.email, 'first_name': admin.first_name})

        message = f"New Advertisement have been arrived.Please visit {url}"
        subject = {
            "subject": "New Advertisement",
            "subheadline": "New Advertisement have been created !!!"
            }

        self.sent_email_now(recipients, message, subject)

    def event_for_complaints(self, instance):
        from apps.user.models import User
        admins = User.objects.filter(is_superuser=True)
        recipient = []
        if instance.created_by is None:
            return
        recipient.append({'email': instance.created_by.email, 'first_name': instance.created_by.first_name})
        for admin in admins:
            recipient.append({'email': admin.email, 'first_name': admin.first_name})
        print(instance.created_by.email)
        message = f"New Claim have been arrived."
        subject = {
            "subject": "New Claim has been raised",
            "subheadline": f"New Claim have been raised by Mr/Mrs {recipient[0].get('first_name')} !!!"
        }
        # import pdb;pdb.set_trace()
        self.sent_email_now(recipient, message, subject)

    def event_for_orders(self, instance):
        from apps.user.models import User
        admins = User.objects.filter(is_superuser=True)

        recipient = []
        recipient.append({'email': instance.dealer.email, 'first_name': instance.dealer.first_name})
        for admin in admins:
            recipient.append({'email': admin.email, 'first_name': admin.first_name})

        message = f"New Order have been Created."
        subject = {
            "subject": "New Order has been Created",
            "subheadline": f"New Order have been created by Mr/Mrs {recipient[0].get('first_name')} !!!"
        }
        # import pdb;pdb.set_trace()
        self.sent_email_now(recipient, message, subject)

    def sent_email_now(self, recipient, message, subject):
        # print("KEY", self.api_key)
        # here the recipient ust be list of dictionary
        receivers = [i for i in recipient]
        # import pdb;pdb.set_trace()

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=receivers,
            sender={"name": "Fegno Technologies", "email": "abhishekfegno@gmail.com"},
            template_id=3,
            params={"name": "Customer", "subheadline": subject.get("subheadline"), "message": message},
            # used to render inside email template
            headers={
                "X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3",
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
