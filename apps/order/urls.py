# New file created 
from django.urls import path

from apps.order.views.salesorder_view import *

urlpatterns = [
    path('quotation/list/', QuotationListView.as_view(), name='quotation-list'),
    path('quotation/<int:pk>/update/', QuotationDetailView.as_view(), name='quotation-update'),
    path('quotation/<int:pk>/delete/', QuotationDeleteView.as_view(), name='quotation-delete'),
    path('order/list/', SalesOrderListView.as_view(), name='salesorder-list'),
    path('order/<int:pk>/update/', SalesOrderDetailView.as_view(), name='salesorder-update'),
    path('order/<int:pk>/delete/', SalesOrderDeleteView.as_view(), name='salesorder-delete'),
    path('invoice/list/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoice/<int:pk>/update/', InvoiceDetailView.as_view(), name='invoice-update'),
    path('invoice/<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice-delete'),

    path('order/line/form/', get_orderline_form, name='get_orderline_form'),
    path('order/detail/<int:order_id>/', get_orderline, name='get_orderline'),
    path('order/detail/<int:order_id>/<int:pk>/update/', get_orderline, name='get_orderline-update'),
    path('order/detail/<int:order_id>/<int:pk>/delete/', SalesOrderDeleteView.as_view(), name='get_orderline-delete'),
    path('invoice/line/detail/<int:order_id>', invoice_detail_edit, name='invoice_detail_edit'),
    path('order/excel/export/<str:slug>/', get_excel_report_order, name='get_excel_report_order'),
    path('cancelled/list/', cancelled_order, name='cancelled_order'),

    path('change/status/<int:pk>/', quotation_status, name='quotation_status'),

    # path('order/status-update/<int:id>/', get_orderline_form, name='order-status-update'),

]
