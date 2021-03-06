from collections import OrderedDict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy, reverse


def PUBLIC_APIS(r, f) -> list:
    def url(name, *args, **kwargs):
        return reverse_lazy(name, kwargs=kwargs, request=r, format=f)

    def _(*args):
        return OrderedDict(args)

    return [

        #
        ("Dealer APIs", OrderedDict([
            ("User Login", reverse('user:user-login', request=r, format=f)),
            ("User Login/Token", reverse('user:user-token-login', request=r, format=f)),
            ("User Logout", reverse('user:user-logout', request=r, format=f)),
            ("User Profile", reverse('user:user-profile', request=r, format=f)),
            ("Password Reset", reverse('user:password-reset', request=r, format=f)),
            ("Password Change", reverse('user:password-change', request=r, format=f)),
            ("Dealer Complaint", reverse('user:dealer-complaints', request=r, format=f)),
            ("Home API", reverse('user:home-page', request=r, format=f)),

            ("Zone List", reverse('user:zone-list', request=r, format=f)),
            ("Branch List", reverse('user:branch-list', request=r, format=f)),
            ("Product List", reverse('catalogue:api-product-list', request=r, format=f)),
            ("Category List", reverse('catalogue:api-category-list', request=r, format=f)),

            ("Order List", reverse('order:api-order-list', request=r, format=f)),
            ("Order Detail", reverse('order:api-order-detail', request=r, format=f, kwargs={'pk': 27})),

            ("Transactions API", reverse('payment:api-transaction-list', request=r, format=f)),
            ("Credit API", reverse('payment:api-credit-list', request=r, format=f)),


            ("Excalation API", reverse('user:escalation_number', request=r, format=f, kwargs={'pk': 1})),
            ("Notification API", reverse('notification:api-notification-list', request=r, format=f)),
            ("Check-in Create API", reverse('executive-tracking-api:check-point-create-api', request=r, format=f)),
            ("Check-in Update API",
             reverse('executive-tracking-api:check-point-update-api', request=r, format=f, kwargs={'pk': 1})),

            # ("Enter OTP", reverse('enter_otp', request=r, format=f)),
            # ("Community List", reverse('operator:communitycarwashextension-list', request=r, format=f)),
            #
            # ("Task List", reverse('operator:task-list', request=r, format=f)),
            # ("Task Detail", reverse('operator:task-detail', request=r, format=f, kwargs={'pk': 2})),

        ])),
        ('Excecutive API', OrderedDict([
            ("Dealers List", reverse('user:dealer-list', request=r, format=f)),
            ("Dealers Detail", reverse('user:dealer-detail', request=r, format=f, kwargs={'pk': 12})),
            ("Order List Executive", reverse('order:api-order-list-executive', request=r, format=f)),

        ])),
        ('Settings & Configurations', OrderedDict([

        ])),
        # ("Notifications", url('user-api:notifications')),
        # ("Static Constants", url('user-api:static_constants')),
        # ("Dynamic Constants", url('user-api:dynamic_constants')),
    ]


@api_view(("GET",))
def api_root(request, format=None):  # pylint: disable=redefined-builtin
    """
    GET:
    Display all available urls.

    Since some urls have specific permissions, you might not be able to access
    them all.
    """

    apis = PUBLIC_APIS(request, format)
    return Response(OrderedDict(apis))
