
from django.urls import path, include

from apps.user.api.viewsets import *

app_name = 'user'
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('profile/', ProfileAPIView.as_view(), name='user-profile'),
    path('complaints/', ComplaintListView.as_view(), name='dealer-complaints'),
]
