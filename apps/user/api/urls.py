
from django.urls import path, include

from apps.user.api.viewsets import *

app_name = 'user'
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('profile/', ProfileAPIView.as_view(), name='user-profile'),
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('complaints/', ComplaintListView.as_view(), name='dealer-complaints'),
    path('homepage/', HomePageAPI.as_view(), name='home-page'),
]
