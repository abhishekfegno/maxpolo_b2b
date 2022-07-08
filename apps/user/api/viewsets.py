from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from apps.catalogue.api.serializers import ProductPDFSerializer, ProductPDFListSerializer
from apps.catalogue.models import PDF
from apps.order.api.serializers import UpcomingPaymentSerializer
from apps.order.models import SalesOrder
from apps.user.api.serializers import LoginSerializer, ProfileAPISerializer, ComplaintSerialzer, \
    PasswordResetSerializer, AdvertisementSerializer, DealerSerializer
from apps.user.models import User, Complaint, Banners, Dealer
from lib.sent_email import EmailHandler
from lib.utils import list_api_formatter, CsrfExemptSessionAuthentication


class ExeDealerMixin(object):
    def get_dealer_id(self):
        if 'dealer_id' in self.request.GET:
            return self.request.GET['dealer_id']
        return self.request.user.id


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({}, status=400)

        user = request.user
        out = {}
        out['user'] = {
            "id": user.id,
            "role_id": user.user_role,
            "role": user.user_role_name,
            "company_name": user.get_full_name(),
            "company_cin": user.company_cin,
            "address_street": user.address_street,
            "address_city": user.address_city,
            "address_state": user.address_state,
            "branch": user.branch and user.branch.name,
            "executive": {
                'name': user.executive.first_name,
            } if user.executive else None,
            "zone": user.zone if user.zone else None,
            "mobile": user.mobile,
        }
        return Response(out)

    def post(self, request, *args, **kwargs):
        out = {}
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            try:
                # u = User.objects.get(email=data['email']).username
                user = authenticate(request, username=data['username'], password=data['password'])
                if user is None:
                    return Response({
                        "status": "Unauthorized!!! "
                    }, status=status.HTTP_401_UNAUTHORIZED)

                login(request, user)
                out['user'] = {
                    "id": user.id,
                    "role_id": user.user_role,
                    "role": user.user_role_name,
                    "company_name": user.get_full_name(),
                    "company_cin": user.company_cin,
                    "address_street": user.address_street,
                    "address_city": user.address_city,
                    "address_state": user.address_state,
                    "branch": user.branch and user.branch.name,
                    "executive": {
                        'name': user.executive.first_name,
                    } if user.executive else None,
                    "zone": None,
                    "mobile": user.mobile,
                }
            except Exception as e:
                out['errors'] = str(e)
                return Response(out, status=status.HTTP_401_UNAUTHORIZED)
        else:
            out['errors'] = serializer.errors
            return Response(out, status=status.HTTP_400_BAD_REQUEST)
        return Response(out, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPIView(GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class DealerListView(ListAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['username']
    ordering_fields = ['username']
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Dealer.objects.all().filter(executive=self.request.user)


class ProfileAPIView(ExeDealerMixin, GenericAPIView):
    queryset = User.objects.all().select_related('branch').prefetch_related('dealers')
    serializer_class = ProfileAPISerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset().get(id=self.get_dealer_id())).data
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


class ComplaintListView(ExeDealerMixin, ListAPIView):
    """
        {
            "title":"asdf",
            "description":"asdfasdfa"
        }
    """
    queryset = Complaint.objects.select_related('created_by', 'order_id')
    serializer_class = ComplaintSerialzer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ()
    search_fields = ()
    ordering_fields = ()
    pagination_class = PageNumberPagination
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # permission_classes = (permissions.IsAuthenticated, )
    parser_classes = (MultiPartParser, FileUploadParser)

    def list(self, request, *args, **kwargs):
        page_number = request.GET.get('page_number', 1)
        page_size = request.GET.get('page_size', 20)


        serializer = self.get_serializer(self.get_queryset().filter(created_by_id=self.get_dealer_id()), many=True, context={'request': request})
        queryset = self.filter_queryset(self.get_queryset())
        paginator = Paginator(queryset, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        page_obj = paginator.get_page(page_number)
        return Response(list_api_formatter(request, paginator=paginator, page_obj=page_obj, results=serializer.data))

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = request.user
            serializer.save()
        else:
            data['errors'] = serializer.errors
        return Response(data)


class HomePageAPI(ExeDealerMixin, APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        # dealer_id = request.GET.get('dealer', request.user.id)
        advertisements = AdvertisementSerializer(Banners.objects.all(), many=True, context={'request': request}).data
        pdf = ProductPDFListSerializer(PDF.objects.select_related('category')[:6], many=True, context={'request': request}).data
        upcoming_payments = UpcomingPaymentSerializer(
            SalesOrder.objects.filter(
                is_invoice=True, dealer_id=self.get_dealer_id(), invoice_status__in=['payment_partial', 'credit']),
            many=True, context={'request': request}).data
        dealer = Dealer.objects.all().filter(pk=self.get_dealer_id()).first()
        result = {
            "banners": advertisements,
            "new arrival": pdf,
            "payment": upcoming_payments,
            "dealer": {
                "id": dealer.id,
                "role": dealer.user_role_name,
                "company_name": dealer.get_full_name(),
                "company_cin": dealer.company_cin,
                "address_street": dealer.address_street,
                "address_city": dealer.address_city,
                "address_state": dealer.address_state,
                "mobile": dealer.mobile,
            } if dealer else None
        }
        return Response(result)
