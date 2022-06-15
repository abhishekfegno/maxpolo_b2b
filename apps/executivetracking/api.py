from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework import mixins, status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

from apps.executivetracking.models import CheckPoint, Lead, CheckInDay, District, CrashReport
from apps.executivetracking.choices import DISTRICTS

from apps.executivetracking.serializers import CheckPointSerializer, LeadSerializer, CheckInDaySerializer, \
    CrashReportSerializer

from apps.catalogue.models import Product

from apps.user.constants import Role
from apps.utils.authentication import CsrfExemptSessionAuthentication, reauthenticate


class IsAuthenticatedExecutive(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.user_role == user.EXECUTIVE)


# {
#     "check_out_at": "2021-02-08T12:55:44.087113Z"
# }
# SRID=4326;POINT(-79.976111 40.374444)


class CrashReportCreate(CreateAPIView):
    serializer_class = CrashReportSerializer
    queryset = CrashReport.objects.all()
    permission_classes = [IsAuthenticatedExecutive]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication, TokenAuthentication]


class CheckPointCreate(ListCreateAPIView):
    serializer_class = CheckPointSerializer
    queryset = CheckPoint.objects.all()
    permission_classes = [IsAuthenticatedExecutive]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return self.queryset.filter(store__executive__user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CheckPointUpdate(RetrieveUpdateAPIView):
    serializer_class = CheckPointSerializer
    queryset = CheckPoint.objects.all()
    permission_classes = [IsAuthenticatedExecutive]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return self.queryset.filter(store__executive__user=self.request.user)


class CheckInDayCreate(mixins.RetrieveModelMixin, ListCreateAPIView):
    serializer_class = CheckInDaySerializer
    queryset = CheckInDay.objects.all()
    permission_classes = [IsAuthenticatedExecutive]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication, TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(executive__user=self.request.user)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = serializer.data
        out = {**response, 'districts': [
            District.objects.filter(branch=request.branch).values('id', 'name').order_by('name')
        ]}
        reauthenticate(request)
        # try to authenticate if remaining session expiry time is less than 10 % of logged in period
        return Response(out, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return response


class CheckInDayUpdate(RetrieveUpdateAPIView):
    serializer_class = CheckInDaySerializer
    queryset = CheckInDay.objects.all()
    permission_classes = [IsAuthenticatedExecutive]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return self.queryset.filter(executive__user=self.request.user)


class LeadList(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, ListCreateAPIView):
    serializer_class = LeadSerializer
    queryset = Lead.objects.filter(dealer_account__isnull=True, is_removed=False)
    permission_classes = [IsAuthenticatedExecutive]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def filter_queryset(self, queryset):
        if self.request.GET.get('q'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('q'))
        if self.request.GET.get('place'):
            queryset = queryset.filter(place__iexact=self.request.GET.get('place'))
        if self.request.user.user_role == self.request.user.EXECUTIVE:
            return queryset.filter(executive__user=self.request.user)
        elif self.request.user.user_role == self.request.user.ADMIN:
            return queryset
        elif self.request.user.user_role < self.request.user.EXECUTIVE:     # top ranker in organization tree
            return queryset.filter(executive__branch=self.request.branch)
        return queryset.none()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DealerList(ListAPIView):
    serializer_class = LeadSerializer
    queryset = Lead.objects.filter(dealer_account__isnull=False, is_removed=False)
    permission_classes = [IsAuthenticatedExecutive]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def filter_queryset(self, queryset):
        if int(self.request.user.user_role) > Role.ADMIN:
            queryset = queryset.filter(dealer_account__branch=self.request.user.account.branch)
        if self.request.GET.get('q'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('q'))
        if self.request.GET.get('place'):
            queryset = queryset.filter(place__iexact=self.request.GET.get('place'))
        if self.request.user.user_role == self.request.user.EXECUTIVE:
            return queryset.filter(executive__user=self.request.user)
        elif self.request.user.user_role == self.request.user.ADMIN:
            return queryset
        elif self.request.user.user_role < self.request.user.EXECUTIVE:  # top ranker in organization tree
            return queryset.filter(executive__branch=self.request.branch)
        return queryset.none()

