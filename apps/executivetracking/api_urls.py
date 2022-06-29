from datetime import time, datetime

from django.conf import settings
from django.urls import path
from django.utils import datetime_safe
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.executivetracking.api import *
from apps.executivetracking.serializers import CheckPointReadSerializer
from apps.user.models import Executive, User

app_name = 'executive-tracking-api'


@api_view()
def district_list(request):
    if request.GET.get('token') == settings.SIGNATURE_AUTHENTICATION:
        return Response({'status': 'unauthenticated'}, status=401)
    if request.user.is_anonymous:
        return Response({'status': 'unauthenticated'}, status=401)
    account = request.user.account

    if request.user.user_role == User.EXECUTIVE:
        places = [*set(account.dealer_set.all().values_list('place', flat=True))]
        return Response({
            'results': [{
                'id': 0,
                'name': place,
                'short_code': ''
            } for place in places]
        }, status=200)
    branch = account and account.branch
    return Response({
        # 'results': District.objects.filter(branch=branch).values('id', 'name', 'short_code').order_by('name')
    }, status=200)


@api_view(['POST'])
def share_lead(request, pk, **kwargs):
    """
    POST 'application/json' {"executives": [2, 3, 4, 5]}
    """
    if request.user.is_anonymous:
        return Response({'status': 'unauthenticated'}, status=401)
    lead = get_object_or_404(Lead, pk=pk)
    executives = Executive.objects.filter(id__in=request.data.get('executives'))
    updated = 0
    lead_backup = lead
    for e in executives:
        lead.pk = None
        lead.id = None
        lead.shared_from = lead_backup
        lead.executive = e
        lead.save()
    return Response({'status': 'success', 'updated': updated})


@api_view()
def admin_summary(request, **kwargs):
    if request.user.is_anonymous:
        return Response({'status': 'unauthenticated'}, status=401)
    executive_id = request.GET.get('executive')
    queryset = Executive.objects.all()
    branch = request.user.account and request.user.account.branch
    if request.user.user_role == Role.EXECUTIVE:
        executive_id = request.user.account.id
        queryset = queryset.filter(**{Executive.branch_filter: branch})
    elif request.user.user_role > Role.ADMIN:
        if branch:
            queryset = queryset.filter(**{Executive.branch_filter: branch})
    object = queryset.filter(pk=executive_id).first()
    kwargs['errors'] = []
    date = request.GET.get('date')
    if not date:
        date = datetime_safe.date.today()
    else:
        try:
            date = datetime_safe.datetime.strptime(date, "%d-%m-%Y").date()
        except:
            date = datetime_safe.date.today()
            kwargs['errors'].append(
                {'invalid_date': f"Invalid date format. Date must be in format '{date.strftime('d-%m-%Y')}'"})
    if object:
        check_in_day = CheckInDay.objects.filter(
            **{'check_in_at__range': (
                datetime.combine(date, time.min),
                datetime.combine(date, time.max)
            )},
            executive=object).order_by('check_in_at')
        check_in = CheckPoint.objects.filter(
            **{'check_in_at__range': (
                datetime.combine(date, time.min),
                datetime.combine(date, time.max)
            )},
            store__executive=object).select_related('store').order_by('check_in_at')
        kwargs['checkin_set'] = (
                CheckInDaySerializer(check_in_day, many=True).data
                + CheckPointReadSerializer(check_in, many=True).data
        )
        kwargs['checkin_set'].sort(
            key=lambda check: datetime_safe.datetime.strptime(check['check_in_at'], "%Y-%m-%dT%H:%M:%S+05:30").date()
        )
        first_device_id = None
        for i in kwargs['checkin_set']:
            if i['device_id']:
                first_device_id = i['device_id']
                break
        kwargs['first_device_id'] = first_device_id
    else:
        kwargs['errors'].append("No Executives Selected!")
        kwargs['checkin_set'] = []
        kwargs['first_device_id'] = None
    kwargs['executive_list'] = [{
        'id': exec.id,
        'name': exec.name,
        'branch': exec.branch.name,
        'system_id': exec.system_id,
    } for exec in queryset.select_related('branch')]
    kwargs['selected_date'] = date.strftime("%d-%m-%Y")

    return Response({
        'results': kwargs
    }, status=200)


urlpatterns = [
    # path('leads/', LeadList.as_view(), name="lead-list-api"),
    # path('dealers/', DealerList.as_view(), name="dealer-list-api"),
    path('check-point/', CheckPointCreate.as_view(), name="check-point-create-api"),
    # path('check-id-today/', CheckInDayCreate.as_view(), name="check-in-day-create-api"),
    path('check-point/<int:pk>/', CheckPointUpdate.as_view(), name="check-point-update-api"),
    # path('check-id-today/<int:pk>/', CheckInDayCreate.as_view(), name="check-in-day-update-api"),
    path('districts/', district_list, name="district-list-api"),
    path('admin-summary/', admin_summary, name="admin-summary-api"),
    path('share-lead/<int:pk>/', share_lead, name="share-lead-api"),
    path('crash-reporting/', CrashReportCreate.as_view(), name="crash-reporting"),

]
