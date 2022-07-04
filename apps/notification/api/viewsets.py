
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView

from apps.notification.api.serializers import NotificationSerializer
from apps.notification.models import Notification


class NotificationAPIView(ListAPIView):
    queryset = Notification.objects.select_related('user')
    serializer_class = NotificationSerializer
    filterset_fields = ['user']
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('order_id', 'invoice_id')

