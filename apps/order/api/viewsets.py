from django.core.paginator import Paginator, EmptyPage
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination as CorePageNumberPagination
from rest_framework.response import Response

from apps.catalogue.models import Product
from apps.order.api.serializers import OrderSerializer, OrderDetailSerializer, OrderCreateSerializer
from apps.order.models import SalesOrder, SalesOrderLine
from apps.payment.models import Transaction
from apps.user.models import Dealer
from lib.sent_email import EmailHandler
from lib.utils import list_api_formatter, CsrfExemptSessionAuthentication


class PageNumberPagination(CorePageNumberPagination):
    page_size = 55


class OrderDetailAPIView(RetrieveAPIView):
    queryset = SalesOrder.objects.all().select_related('dealer').prefetch_related('line', 'line__product', 'transaction_set')
    serializer_class = OrderDetailSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ['is_cancelled', 'is_confirmed', 'is_invoice', 'is_quotation']
    search_fields = ('order_id', 'invoice_id')
    ordering_fields = ()
    pagination_class = PageNumberPagination


class OrderListAPIExecutiveView(ListAPIView):
    """
    filters
        ?is_quotation=True
        ?is_confirmed=True
        ?is_invoice=True
    POST data
    {
        "products":[1,2,3],
        "quantites":[1,2,3],
        "dealer":3
    }
    """
    queryset = SalesOrder.objects.all().select_related('dealer').prefetch_related('line', 'line__product', 'transaction_set').order_by('-created_at')
    serializer_class = OrderSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ['is_cancelled', 'is_confirmed', 'is_invoice', 'is_quotation']
    search_fields = ('order_id', 'invoice_id')
    ordering_fields = ()
    pagination_class = PageNumberPagination
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def filter_queryset(self, queryset):
        filt = {k: v for k, v in self.request.query_params.items()}
        # import pdb;pdb.set_trace()
        qs = queryset
        if 'dealer_id' in filt:
            qs = qs.filter(dealer_id=filt.get('dealer_id'))
        if 'is_quotation' in filt:
            qs = qs.filter(is_quotation=True).order_by('-created_at')
        if 'is_cancelled' in filt:
            qs = qs.filter(is_cancelled=True).order_by('-created_at')
        if 'is_confirmed' in filt:
            qs = qs.filter(is_confirmed=True).order_by('-confirmed_date')
        if 'is_invoice' in filt:
            qs = qs.filter(is_invoice=True).order_by('-invoice_date')
        return qs

    def list(self, request, *args, **kwargs):

        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        # import pdb;pdb.set_trace()
        queryset = self.filter_queryset(self.get_queryset())

        paginator = Paginator(queryset, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        page_obj = paginator.get_page(page_number)
        serializer = self.get_serializer(page_obj.object_list, many=True, context={'request': request})
        return Response(list_api_formatter(request, paginator=paginator, page_obj=page_obj, results=serializer.data))

    # def post(self, request, *args, **kwargs):
    #     result = {}
    #     dealer = request.data.get('dealer', request.user.id)
    #     print(dealer)
    #     quantity = request.data.getlist('products')
    #     products = request.data.getlist('quantites')
    #     serializer = self.get_serializer(data=request.data)
    #     try:
    #         order = SalesOrder.objects.create(dealer=Dealer.objects.get(id=dealer))
    #         for product, quantity in zip(products, quantity):
    #             line = SalesOrderLine.objects.create(product=Product.objects.get(id=product), quantity=quantity,
    #                                                  order=order)
    #             print(f"line created {line} for order {order}")
    #         EmailHandler().sent_mail_order(order)
    #     except Exception as e:
    #         result['errors'] = str(e)
    #     return Response(result, status=status.HTTP_200_OK)


class OrderListAPIView(CreateModelMixin, ListAPIView):
    """
    GET:
    /.../.../../?is_cancelled=1
    /.../.../../?is_confirmed=1
    /.../.../../?is_invoice=1
    /.../.../../?is_quotation=1

    POST:

    {
        "dealer" : <dealer_id>,
        "line": [{
            "product": <product_id>,
            "quantity": 8
        }, {...}, {...}]
    }

    """
    queryset = SalesOrder.objects.all().select_related('dealer').prefetch_related('line', 'line__product',
                              Prefetch('transaction_set', queryset=Transaction.objects.all())).order_by('-created_at')

    def get_serializer_class(self, data=None):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    pagination_class = PageNumberPagination
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated, )
    filterset_fields = ['is_cancelled', 'is_confirmed', 'is_invoice', 'is_quotation']
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('order_id', 'invoice_id')

    def filter_queryset(self, queryset):
        filt = {k: v for k, v in self.request.query_params.items()}
        qs = queryset.filter(dealer=self.request.user)
        if 'is_quotation' in filt:
            qs = qs.filter(is_quotation=True).order_by('-created_at')
        if 'is_cancelled' in filt:
            qs = qs.filter(is_cancelled=True).order_by('-created_at')
        if 'is_confirmed' in filt:
            qs = qs.filter(is_confirmed=True).order_by('-confirmed_date')
        if 'is_invoice' in filt:
            qs = qs.filter(is_invoice=True).order_by('-invoice_date')
        return qs

    def list(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        # import pdb;pdb.set_trace()
        queryset = self.filter_queryset(self.get_queryset())
        paginator = Paginator(queryset, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        page_obj = paginator.get_page(page_number)
        serializer = self.get_serializer(page_obj.object_list, many=True, context={'request': request})
        return Response(list_api_formatter(request, paginator=paginator, page_obj=page_obj, results=serializer.data))

    def post(self, request, *args, **kwargs):
        data = {}
        self.serializer_class = self.get_serializer_class()
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
        else:
            data['errors'] = serializer.errors
        return Response(data)


