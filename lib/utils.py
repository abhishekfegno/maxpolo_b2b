import random
from collections import OrderedDict

from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination as CorePageNumberPagination


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        return  # To not perform the csrf check previously happening


class PageNumberPagination(CorePageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50

    # def get_paginated_response(self, data):
    #     return Response(collections.OrderedDict([
    #         ('lastPage', self.page.paginator.count),
    #         ('countItemsOnPage', self.page_size),
    #         ('current', self.page.number),
    #         ('next', self.get_next_link()),
    #         ('previous', self.get_previous_link()),
    #         ('results', data)
    #     ]))


def yes_no(val):
    return ["no", "yes"][bool(val)]


def generate_random_number(length):
    return "".join(random.choices('1234567890', k=length))


def model_id_to_string(number, prefix, _width=6):
    return '#' + prefix + str(number).zfill(_width)


def generate_path(request, **kwargs):
    path = request._request.path_info
    b = request.build_absolute_uri
    return b("{}?{}".format(
        path,
        "&".join(
            [f"{k}={kwargs.get(k)}" for k in kwargs.keys() if kwargs.get(k)]
        )
    ))


def list_api_formatter(request, paginator, page_obj, results=None, **kwargs):
    next_url = prev_url = None
    if results is None:
        results = page_obj.object_list
    params = {k: request.GET.get(k) for k, v in request.GET.items()}
    if page_obj.has_next():
        params['page'] = page_obj.next_page_number()
        next_url = generate_path(request, **params)

    if page_obj.has_previous():
        params['page'] = page_obj.previous_page_number()
        prev_url = generate_path(request, **params)
    # out = paginator.get_paginated_response_context(results)
    count = len(results)
    return OrderedDict([
        ('count', paginator.count),
        ('num_pages', paginator.num_pages),
        ('next_url', next_url),
        ('prev_url', prev_url),
        ('results', results),
        *kwargs.items()
    ])


def get_local_time(date):
    from django.utils.timezone import localtime
    # import pdb;pdb.set_trace()
    if date:
        return date.strftime("%d-%b-%Y %H:%M %p")
    return None
