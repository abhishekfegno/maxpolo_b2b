from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.user.api.serializers import LoginSerializer, ProfileAPISerializer, ComplaintSerialzer
from apps.user.models import User, Complaint
from lib.utils import list_api_formatter



class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        out = {}
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = authenticate(request, username=data['username'], password=data['password'])
            try:
                login(request, user)
            except Exception as e:
                out['errors'] = str(e)
            print(user, request.user)
        else:
            out['errors'] = serializer.errors
        return Response(serializer.data)




class ProfileAPIView(GenericAPIView):
    queryset = User.objects.all().select_related('branch').prefetch_related('dealers')
    serializer_class = ProfileAPISerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset().get(id=request.user.id))
        return Response(serializer.data)


class ComplaintListView(ListAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerialzer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ()
    search_fields = ()
    ordering_fields = ()
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        page_number = request.GET.get('page_number', 1)
        page_size = request.GET.get('page_size', 20)
        serializer = self.get_serializer(self.get_queryset(), many=True, context={'request': request})
        queryset = self.filter_queryset(self.get_queryset())
        paginator = Paginator(queryset, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        page_obj = paginator.get_page(page_number)
        return Response(list_api_formatter(request, paginator=paginator, page_obj=page_obj, results=serializer.data))


