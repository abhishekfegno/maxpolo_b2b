from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, register_converter
from django.urls.converters import SlugConverter

from .models import Role
from .views.banners_view import *
from .views.complaint_view import *
from .views.user_view import *


class ExecDealer(SlugConverter):

    def to_python(self, value):
        return value

    def to_url(self, value):
        if Role.EXECUTIVE == value:
            return 'executive'

        if Role.DEALER == value:
            return 'dealer'

        return value


register_converter(ExecDealer, 'role')

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

    path('user/list/<role:role>/', UserListView.as_view(), name='user-list'),
    path('user/<role:role>/<int:pk>/update/', UserListView.as_view(), name='user-update'),
    path('user/<role:role>/<int:pk>/password/', UserPasswordView.as_view(), name='user-password'),
    path('user/<role:role>/<int:pk>/delete/', UserListView.as_view(), name='user-delete'),

    path('zone/list/', ZoneView.as_view(), name='zone-list'),
    path('zone/<int:pk>/update/', ZoneUpdateView.as_view(), name='zone-update'),
    path('zone/<int:pk>/delete/', ZoneDeleteView.as_view(), name='zone-delete'),

    path('escalation/list/', EscalationNumberView.as_view(), name='escalation-list'),
    # path('escalation/<int:pk>/delete/', EscalationNumberView.as_view(), name='zone-update'),



    path('complaint/excel/export/', get_excel_report_complaint, name='get_excel_report_complaint')

]
