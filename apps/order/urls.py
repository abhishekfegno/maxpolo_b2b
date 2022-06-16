# New file created 
from django.urls import path, include

from apps.order.views.salesorder_view import *


urlpatterns = [
    path('order/list', SalesOrderListView.as_view(), name='salesorder-list'),
    path('order/<int:pk>/update/', SalesOrderDetailView.as_view(), name='salesorder-update'),
    path('order/<int:pk>/delete/', SalesOrderDeleteView.as_view(), name='salesorder-delete'),

    path('order/line/form/', get_orderline_form, name='get_orderline_form'),

]


