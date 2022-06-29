from django.urls import path

from apps.order.api.viewsets import OrderListAPIView, OrderDetailAPIView

app_name = 'order'
urlpatterns = [
    path('order/list/', OrderListAPIView.as_view(), name='api-order-list'),
    path('order/detail/<int:pk>/', OrderDetailAPIView.as_view(), name='api-order-detail'),
]
