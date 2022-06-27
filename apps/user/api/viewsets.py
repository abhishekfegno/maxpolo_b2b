from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from apps.catalogue.api.serializers import ProductPDFSerializer
from apps.catalogue.models import PDF
from apps.user.api.serializers import LoginSerializer, ProfileAPISerializer, ComplaintSerialzer, \
    PasswordResetSerializer, AdvertisementSerializer, DealerSerializer
from apps.user.models import User, Complaint, Banners, Dealer
from lib.sent_email import EmailHandler
from lib.utils import list_api_formatter
from django.contrib.auth import logout


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        out = {}
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            try:
                u = User.objects.get(email=data['email']).username
                user = authenticate(request, username=u, password=data['password'])
                login(request, user)
                print(user, request.user)
                out['user'] = {
                    "role": user.user_role_name,
                    "company_name": user.username,
                    "zone": user.zone
                }
            except Exception as e:
                out['errors'] = str(e)
                return Response(out, status=status.HTTP_401_UNAUTHORIZED)


        else:
            out['errors'] = serializer.errors
            return Response(out, status=status.HTTP_400_BAD_REQUEST)
        return Response(out, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class DealerListView(ListAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['username']
    ordering_fields = ['username']





class ProfileAPIView(GenericAPIView):
    queryset = User.objects.all().select_related('branch').prefetch_related('dealers')
    serializer_class = ProfileAPISerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset().get(id=request.user.id)).data
            result = serializer
        except Exception as e:
            result = {str(e)}
        return Response(result)

    def put(self, request, *args, **kwargs):
        result = {}
        serializer = self.get_serializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            result['errors'] = serializer.errors
        return Response(result, status=status.HTTP_200_OK)


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        result = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = EmailHandler()
            recipient = {"email": serializer.data['email'], "name": serializer.data["username"]}
            subject = {
                "subject": "Password Reset",
                "subheadline": "You have requested for a Password Reset"
            }
            try:
                user = User.objects.get(username=serializer.data["username"])
                token, _ = Token.objects.get_or_create(user=user)

                _url = reverse('password-reset-page', request=request, format=None, kwargs={"token": token.key})
                # url = f"{reverse('password_reset-', request=request, format=None)}/{token.key}/"
                message = f'You can reset you password by visiting this link {_url}'
                email.sent_email_now(recipient, message, subject)
                print(token)
            except Exception as e:
                result["message"] = str(e)
            result["message"] = "Email sent"
        return Response(result)


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

    def post(self, request, *args, **kwargs):
        data = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            EmailHandler().sent_mail_complaint(instance)
        else:
            data['errors'] = serializer.errors
        return Response(data)


class HomePageAPI(APIView):

    def get(self, request, *args, **kwargs):
        advertisements = AdvertisementSerializer(Banners.objects.all(), many=True, context={'request': request}).data
        pdf = ProductPDFSerializer(PDF.objects.all(), many=True, context={'request': request}).data
        result = {
            "banners": advertisements,
            "new arrival": pdf,
            "payment": "Payment"
        }
        return Response(result)
