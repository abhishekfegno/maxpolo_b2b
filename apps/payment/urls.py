# New file created 
from django.urls import path

from .views import *

urlpatterns = [
    path('transaction/list', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/<int:pk>/update/', TransactionDetailView.as_view(), name='transaction-update'),
    path('quotation/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction-delete'),

    path('payment/excel/export/', get_excel_report_payment, name='get_excel_report_payment'),

]
