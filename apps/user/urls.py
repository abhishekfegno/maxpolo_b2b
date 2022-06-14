from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from .views import *
from .views.banners_view import *
from .views.complaint_view import *

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='paper/index.html')), name='index'),

    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/login.html'), name='logout'),
    path('setpassword/<slug:token>/', password_reset, name='password_reset'),


    path('complaint/list/', ComplaintListView.as_view(), name='complaint-list'),
    path('complaint/<int:pk>/update/', ComplaintDetailView.as_view(), name='complaint-update'),
    path('complaint/<int:pk>/delete/', ComplaintDeleteView.as_view(), name='complaint-delete'),
    path('banners/list/', BannersListView.as_view(), name='banners-list'),
    path('banners/<int:pk>/update/', BannersDetailView.as_view(), name='banners-update'),
    path('banners/<int:pk>/delete/', BannersDeleteView.as_view(), name='banners-delete'),
]
