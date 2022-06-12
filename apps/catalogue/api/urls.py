
from django.urls import path, include

from apps.catalogue.api.viewsets import ProductAPIView

app_name = 'catalogue'
urlpatterns = [
    path('product/list/', ProductAPIView.as_view(), name='api-product-list'),
]
