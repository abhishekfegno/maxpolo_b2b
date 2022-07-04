from django.urls import path

from apps.notification.api.viewsets import *
app_name = 'notification'

urlpatterns = [
    path('notification/list/', NotificationAPIView.as_view(), name='api-notification-list'),
    # path('order/detail/<int:pk>/', OrderDetailAPIView.as_view(), name='api-order-detail'),
]
