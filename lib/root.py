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
            ("Product List", reverse('catalogue:api-product-list', request=r, format=f)),
        #     ("Enter OTP", reverse('enter_otp', request=r, format=f)),
        #     ("Community List", reverse('operator:communitycarwashextension-list', request=r, format=f)),
        #
        #     ("Task List", reverse('operator:task-list', request=r, format=f)),
        #     ("Task Detail", reverse('operator:task-detail', request=r, format=f, kwargs={'pk': 2})),

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

