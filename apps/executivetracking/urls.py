from django.urls import path, include

from apps.executivetracking.views import *

urlpatterns = [
    path('field-force/excel/download/', get_fieldforce_excel, name="get_fieldforce_excel"),
    path('field-force/', FieldForceSelect.as_view(), name="field-force-tracking"),
    path('field-force/<int:pk>/', FieldForceTracking.as_view(), name="field-force-tracking-detail"),
    path('leads/', LeadListView.as_view(), name="leads-list"),
    path('leads/<int:pk>/', LeadListView.as_view(), name="leads-exec-list"),
    path(f'district/', include([
        path(f'', DistrictList.as_view(), name="district-list"),
        path('create/', DistrictCreateView.as_view(), name="district-create"),
        path('update/<int:pk>/', DistrictUpdateView.as_view(), name="district-update"),
    ])),

]
