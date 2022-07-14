from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from apps.catalogue.api.serializers import ProductPDFSerializer, ProductPDFListSerializer
from apps.catalogue.models import PDF
from apps.executivetracking.models import Zone
from apps.infrastructure.models import Branch
from apps.order.api.serializers import UpcomingPaymentSerializer
from apps.order.models import SalesOrder
from apps.user.api.serializers import LoginSerializer, ProfileAPISerializer, ComplaintSerialzer, \
    PasswordResetSerializer, AdvertisementSerializer, DealerSerializer, DealerDetailSerializer, \
    ExcalationNumberSerializer, ZoneSerializer, BranchSerializer, PasswordChangeSerializer
from apps.user.models import User, Complaint, Banners, Dealer, SiteConfiguration
from lib.sent_email import EmailHandler
from lib.utils import list_api_formatter, CsrfExemptSessionAuthentication


class ExeDealerMixin(object):
    def get_dealer_id(self):
        if 'dealer_id' in self.request.GET:
            return self.request.GET['dealer_id']
        return self.request.user.id


class TokenLoginView(ObtainAuthToken):

    def put(self, request, *args, **kwargs):
        """
            {
            "user_id":4
            "logout":True
            }
        """
        logout = request.POST.get('logout')
        if logout:
            Token.objects.get(user_id=request.POST.get('user_id')).delete()
            return Response({"message": "Logout Successfully"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
          {
            username:,
            password:
        }
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        # import pdb;pdb.set_trace()
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
        }, status=status.HTTP_202_ACCEPTED)


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
            "zone": user.zone.name if user.zone else None,
            "mobile": user.mobile,
        }
        # print(user.zone)
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
                    "email": user.email,
                    "mobile": user.mobile,
                    "company_name": user.get_full_name(),
                    "company_cin": user.company_cin,
                    "address_street": user.address_street,
                    "address_city": user.address_city,
                    "address_state": user.address_state,
                    "branch": user.branch and user.branch.name,
                    "executive": {
                        'name': user.executive.first_name,
                        'mobile': user.executive.mobile,
                        'email': user.executive.email,
                        'designation': user.executive.designation,
                    } if user.executive else None,
                    "zone": user.zone.name if user.zone else None,
                }
            except Exception as e:
                out['errors'] = str(e)
                return Response(out, status=status.HTTP_401_UNAUTHORIZED)
        else:
            out['errors'] = serializer.errors
            return Response(out, status=status.HTTP_400_BAD_REQUEST)
        print(user.zone)
        return Response(out, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPIView(GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class DealerListView(ListAPIView):
    queryset = Dealer.objects.all().select_related('zone')
    serializer_class = DealerSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['username']
    ordering_fields = ['username']
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Dealer.objects.all().filter(executive=self.request.user)

    def list(self, request, *args, **kwargs):
        # page_number = request.GET.get('page', 1)
        # page_size = request.GET.get('page_size', 20)
        # # import pdb;pdb.set_trace()
        # queryset = self.filter_queryset(self.get_queryset())
        #
        # paginator = Paginator(queryset, page_size)
        # try:
        #     page_number = paginator.validate_number(page_number)
        # except EmptyPage:
        #     page_number = paginator.num_pages
        # page_obj = paginator.get_page(page_number)
        data = {}
        serializer = self.get_serializer(self.get_queryset(), many=True, context={'request': request})
        data['results'] = serializer.data
        return Response(data)



class DealerDetailView(RetrieveAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerDetailSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['username']
    ordering_fields = ['username']
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated, )

    # def get_queryset(self):
    #     return Dealer.objects.all().filter(executive=self.request.user)


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

    def post(self, request, *args, **kwargs):
        result = {}
        serializer = self.get_serializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            result['errors'] = serializer.errors
        return Response(result, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):
        result = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = EmailHandler()
            subject = {
                "subject": "Password Reset",
                "subheadline": "You have requested for a Password Reset"
            }
            try:
                user = User.objects.filter(email=serializer.data['email']).first()
                token, _ = Token.objects.get_or_create(user=user)
                print(f"Token created:{token}")
                recipient = [{"email": user.email, "name": user.username}]
                _url = reverse('password-reset-page', request=request, format=None, kwargs={"token": token.key})
                message = f'You can reset you password by visiting this link {_url}'
                email.sent_email_now(recipient, message, subject)
                result["message"] = f"Email sent to {recipient}, Token created:{_},{token}"

            except Exception as e:
                result["message"] = str(e)
        return Response(result)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordChangeAPIView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):
        result = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = self.request.user
                # import pdb;pdb.set_trace()
                user.set_password(serializer.data['confirm_password'])
                user.save()
                act_status = status.HTTP_200_OK
            except Exception as e:
                result['errors'] = str(e)
                act_status = status.HTTP_400_BAD_REQUEST
        else:
            result['errors'] = serializer.errors
            act_status = status.HTTP_400_BAD_REQUEST
        return Response(result, status=act_status)


class ComplaintListView(ExeDealerMixin, ListAPIView):
    """
        {
            "title":"asdf",
            "description":"asdfasdfa"
        }
    """
    queryset = Complaint.objects.all().select_related('created_by', 'order_id')
    serializer_class = ComplaintSerialzer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ()
    search_fields = ()
    ordering_fields = ()
    pagination_class = PageNumberPagination
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # permission_classes = (permissions.IsAuthenticated, )
    # parser_classes = (MultiPartParser, FileUploadParser)

    def list(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        queryset = self.filter_queryset(self.get_queryset().filter(created_by=self.get_dealer_id()))
        paginator = Paginator(queryset, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        page_obj = paginator.get_page(page_number)
        serializer = self.get_serializer(page_obj.object_list, many=True, context={'request': request})
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


class ExcalationNumberView(RetrieveAPIView):
    queryset = SiteConfiguration.objects.all()
    serializer_class = ExcalationNumberSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    # def put(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return Response()


class BranchAPIView(ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class ZoneAPIView(ListAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
