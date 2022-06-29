from django.urls import path

from apps.catalogue.api.viewsets import ProductAPIView, CategoryAPIView

app_name = 'catalogue'

urlpatterns = [
    path('product/list/', ProductAPIView.as_view(), name='api-product-list'),
    path('category/list/', CategoryAPIView.as_view(), name='api-category-list'),
]
