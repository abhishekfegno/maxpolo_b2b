
from django.urls import path, include

from apps.payment.api.viewsets import TransactionListAPIView

app_name = 'payment'
urlpatterns = [
    path('transaction/list/', TransactionListAPIView.as_view(), name='api-transaction-list'),
]