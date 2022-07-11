from django.urls import path

from apps.user.api.viewsets import *

app_name = 'user'
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('logout/', LogoutAPIView.as_view(), name='user-logout'),
    path('profile/', ProfileAPIView.as_view(), name='user-profile'),
    path('dealers/list/', DealerListView.as_view(), name='dealer-list'),
    path('dealers/list/<int:pk>/', DealerDetailView.as_view(), name='dealer-detail'),
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('complaints/', ComplaintListView.as_view(), name='dealer-complaints'),
    path('homepage/', HomePageAPI.as_view(), name='home-page'),
    path('branch/list/', BranchAPIView.as_view(), name='branch-list'),
    path('zone/list/', ZoneAPIView.as_view(), name='zone-list'),
    path('excalation_number/list/<int:pk>/', ExcalationNumberView.as_view(), name='escalation_number'),

]
