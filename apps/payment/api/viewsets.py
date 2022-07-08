from django.core.paginator import Paginator, EmptyPage
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.order.models import SalesOrder
from apps.payment.api.serializers import TransactionSerializer, TransactionListSerializer
from apps.payment.models import Transaction
from lib.utils import list_api_formatter


class TransactionListAPIView2(ListAPIView):
    """
    """
    queryset = Transaction.objects.all().select_related('order').order_by('created_at')
    serializer_class = TransactionSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = []
    search_fields = ()
    ordering_fields = ()
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)
        # import pdb;pdb.set_trace()
        queryset = self.filter_queryset(self.get_queryset())

        paginator = Paginator(queryset, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        page_obj = paginator.get_page(page_number)
        serializer = self.get_serializer(page_obj.object_list, many=True, context={'request': request})
        results = {}
        results['total_remaining_amount'] = SalesOrder.objects.filter(is_invoice=True,
                                                                      invoice_status='payment_partial').aggregate(
            Sum('invoice_remaining_amount'))
        results['data'] = serializer.data
        return Response(list_api_formatter(request, paginator=paginator, page_obj=page_obj, results=results))

    # def post(self, request, *args, **kwargs):
    #     result = {}
    #     dealer = request.data.get('dealer')
    #     quantity = request.data.get('products')
    #     products = request.data.get('quantites')
    #     serializer = self.get_serializer(data=request.data)
    #     try:
    #         order = SalesOrder.objects.create(dealer=Dealer.objects.get(id=dealer))
    #         for product, quantity in zip(products, quantity):
    #             line = SalesOrderLine.objects.create(product=Product.objects.get(id=product), quantity=quantity,
    #                                                  order=order)
    #             print(f"line created {line} for order {order}")
    #     except Exception as e:
    #         result['errors'] = str(e)
    #     return Response(result, status=status.HTTP_200_OK)


class TransactionListAPIView(ListAPIView):
    queryset = SalesOrder.objects.filter(is_invoice=True)
    serializer_class = TransactionListSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = []
    search_fields = ()
    ordering_fields = ()
    pagination_class = PageNumberPagination


    def filter_queryset(self, queryset):
        filt = {k: v for k, v in self.request.query_params.items()}
        if self.request.user.user_role == 32:
            print(self.request.user.user_role)
            qs = queryset.filter(dealer=self.request.user).exclude(transaction=None)
        else:
            # user is executive

            if 'dealer_id' and 'is_credit' in filt:
                dealer_id = filt.get('dealer_id')
                queryset.filter(invoice_remaining_amount__gte=0, dealer_id=dealer_id).select_related(
                    'dealer').order_by('invoice_date')
        if 'is_credit' in filt:
            queryset.filter(invoice_status__in=['credit', 'payment_partial']).select_related('dealer').order_by('invoice_date')
            # import pdb;
            # pdb.set_trace()
        if 'is_dealer' in filt:
            dealer_id = filt.get('dealer_id')
            queryset.filter(dealer_id=dealer_id).select_related('dealer').order_by('invoice_date')

        return queryset

    def list(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)
        # import pdb;pdb.set_trace()
        queryset = self.filter_queryset(self.get_queryset())
        paginator = Paginator(queryset, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        page_obj = paginator.get_page(page_number)
        serializer = self.get_serializer(page_obj.object_list, many=True, context={'request': request})
        results = {}
        results['total_remaining_amount'] = queryset.filter(invoice_status='payment_partial').aggregate(
            Sum('invoice_remaining_amount')) or 0
        results['data'] = serializer.data
        return Response(list_api_formatter(request, paginator=paginator, page_obj=page_obj, results=results))