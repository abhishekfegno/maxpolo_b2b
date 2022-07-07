from django.urls import path

from apps.order.api.viewsets import OrderListAPIView, OrderDetailAPIView, OrderListAPIExecutiveView

app_name = 'order'
urlpatterns = [
    path('order/list/executive/', OrderListAPIExecutiveView.as_view(), name='api-order-list-executive'),
    path('order/list/', OrderListAPIView.as_view(), name='api-order-list'),
    path('order/detail/<int:pk>/', OrderDetailAPIView.as_view(), name='api-order-detail'),
]
