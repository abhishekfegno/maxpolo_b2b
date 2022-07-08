from django.urls import path

from apps.payment.api.viewsets import TransactionListAPIView, CreditListAPIView

app_name = 'payment'
urlpatterns = [
    path('credit/list/', CreditListAPIView.as_view(), name='api-credit-list'),
    path('transaction/list/', TransactionListAPIView.as_view(), name='api-transaction-list'),
]
