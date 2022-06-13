from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.user.api.serializers import LoginSerializer
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

