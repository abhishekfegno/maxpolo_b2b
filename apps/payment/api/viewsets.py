from django.core.paginator import Paginator, EmptyPage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.payment.api.serializers import TransactionSerializer
from apps.payment.models import Transaction
from lib.utils import list_api_formatter


class TransactionListAPIView(ListAPIView):
    """
    """
    queryset = Transaction.objects.all().select_related('order')
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

        return Response(list_api_formatter(request, paginator=paginator, page_obj=page_obj, results=serializer.data))

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
