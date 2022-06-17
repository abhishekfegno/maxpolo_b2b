
from django.urls import path, include

from apps.catalogue.api.viewsets import ProductAPIView
from apps.order.api.viewsets import OrderListAPIView

app_name = 'order'
urlpatterns = [
    path('order/list/', OrderListAPIView.as_view(), name='api-order-list'),
]
