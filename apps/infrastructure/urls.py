# New file created 
from django.urls import path, include

from apps.infrastructure.views.branch_view import *

urlpatterns = [
    path('branch/list/', BranchListView.as_view(), name='branch-list'),
    path('branch/<int:pk>/update/', BranchDetailView.as_view(), name='branch-update'),
    path('branch/<int:pk>/delete/', BranchDeleteView.as_view(), name='branch-delete'),

]

