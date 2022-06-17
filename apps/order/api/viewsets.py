from django.core.paginator import Paginator, EmptyPage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.catalogue.api.serializers import ProductSerializer
from apps.catalogue.models import Product
from apps.order.api.serializers import OrderSerializer
from apps.order.models import SalesOrder
from lib.utils import list_api_formatter


class OrderSerializerAPIView(ListAPIView):
    """
    POST data
    {
        "product":[1,2,3],
        "quantity":[1,2,3],
        "dealer":1
    }

    """
    queryset = SalesOrder.objects.all().select_related('dealer').prefetch_related('line', 'line__product')
    serializer_class = OrderSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ('is_cancelled', 'is_confirmed', 'is_invoice')
    search_fields = ('order_id', 'invoice_id')
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
        dealer_id = request.data.get('dealer')
        quantity = request.data.get('dealer')
        product = request.data.get('dealer')
        for product, quantity in zip(products, quantities):
            import pdb;
            pdb.set_trace()

        pass
