
from django.urls import path, include

from apps.catalogue.api.viewsets import ProductAPIView
from apps.order.api.viewsets import OrderSerializerAPIView

app_name = 'order'
urlpatterns = [
    path('order/list/', OrderSerializerAPIView.as_view(), name='api-order-list'),
]
