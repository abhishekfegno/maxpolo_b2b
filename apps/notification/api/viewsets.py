from django.core.paginator import Paginator, EmptyPage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.notification.api.serializers import NotificationSerializer
from apps.notification.models import Notification
from lib.utils import list_api_formatter


class NotificationAPIView(ListAPIView):
    queryset = Notification.objects.select_related('user')
    serializer_class = NotificationSerializer
    filterset_fields = ['user']
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('order_id', 'invoice_id')

    def list(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        queryset = self.filter_queryset(self.get_queryset().filter(user=self.request.user))

        paginator = Paginator(queryset, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        page_obj = paginator.get_page(page_number)
        serializer = self.get_serializer(page_obj.object_list, many=True,
                                         context={'request': request})
        return Response(list_api_formatter(request, paginator=paginator, page_obj=page_obj, results=serializer.data))
