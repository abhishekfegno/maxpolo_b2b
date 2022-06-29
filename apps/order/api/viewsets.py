from django.core.paginator import Paginator, EmptyPage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.catalogue.models import Product
from apps.order.api.serializers import OrderSerializer, OrderDetailSerializer
from apps.order.models import SalesOrder, SalesOrderLine
from apps.user.models import Dealer
from lib.sent_email import EmailHandler
from lib.utils import list_api_formatter, CsrfExemptSessionAuthentication


class OrderDetailAPIView(RetrieveAPIView):
    queryset = SalesOrder.objects.all().select_related('dealer').prefetch_related('line', 'line__product')
    serializer_class = OrderDetailSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ['is_cancelled', 'is_confirmed', 'is_invoice', 'is_quotation']
    search_fields = ('order_id', 'invoice_id')
    ordering_fields = ()
    pagination_class = PageNumberPagination


class OrderListAPIView2(ListAPIView):
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
    queryset = SalesOrder.objects.all().select_related('dealer').prefetch_related('line', 'line__product')
    serializer_class = OrderSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ['is_cancelled', 'is_confirmed', 'is_invoice', 'is_quotation']
    search_fields = ('order_id', 'invoice_id')
    ordering_fields = ()
    pagination_class = PageNumberPagination
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

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
        result = {}
        dealer = request.data.get('dealer', request.user.id)
        print(dealer)
        quantity = request.data.getlist('products')
        products = request.data.getlist('quantites')
        serializer = self.get_serializer(data=request.data)
        try:
            order = SalesOrder.objects.create(dealer=Dealer.objects.get(id=dealer))
            for product, quantity in zip(products, quantity):
                line = SalesOrderLine.objects.create(product=Product.objects.get(id=product), quantity=quantity,
                                                     order=order)
                print(f"line created {line} for order {order}")
            EmailHandler().sent_mail_order(order)
        except Exception as e:
            result['errors'] = str(e)
        return Response(result, status=status.HTTP_200_OK)


class OrderListAPIView(ListAPIView):
    queryset = SalesOrder.objects.all().select_related('dealer').prefetch_related('line', 'line__product')
    serializer_class = OrderSerializer
    pagination_class = PageNumberPagination
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated, )
    filterset_fields = ['is_cancelled', 'is_confirmed', 'is_invoice', 'is_quotation']

    def filter_queryset(self, queryset):
        return queryset.filter(created_by=self.request.user).filter(**{k: v for k, v in self.request.GET.items() if k in self.filterset_fields})


