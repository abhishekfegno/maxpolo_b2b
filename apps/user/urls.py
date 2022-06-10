from django.urls import path, include
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='paper/index.html'), name='index'),
    ]
