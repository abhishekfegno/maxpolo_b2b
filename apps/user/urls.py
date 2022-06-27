from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from .views import *
from .views.user_view import *
from .views.banners_view import *
from .views.complaint_view import *
from ..order.views.salesorder_view import QuotationListView

urlpatterns = [
    # path('', login_required(TemplateView.as_view(template_name='paper/index.html')), name='index'),
    path('', login_required(IndexView.as_view(template_name='paper/index.html')), name='index'),
    # path('', QuotationListView.as_view(), name='quotation_list'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('setpassword/<slug:token>/', password_reset, name='password-reset-page'),


    path('complaint/list/', ComplaintListView.as_view(), name='complaint-list'),
    path('complaint/<int:pk>/update/', ComplaintDetailView.as_view(), name='complaint-update'),
    path('complaint/<int:pk>/delete/', ComplaintDeleteView.as_view(), name='complaint-delete'),
    path('banners/list/', BannersListView.as_view(), name='banners-list'),
    path('banners/<int:pk>/update/', BannersDetailView.as_view(), name='banners-update'),
    path('banners/<int:pk>/delete/', BannersDeleteView.as_view(), name='banners-delete'),
    path('user/list/<int:role>/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/update/', UserDetailView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),

    path('complaint/excel/export/', get_excel_report_complaint, name='get_excel_report_complaint')
]
