from django.core.paginator import Paginator, EmptyPage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.catalogue.api.serializers import ProductSerializer
from apps.catalogue.models import Product
from lib.utils import list_api_formatter


class ProductAPIView(ListAPIView):
    queryset = Product.objects.select_related('category', 'brand')
    serializer_class = ProductSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ('product_code', 'name')
    search_fields = ('product_code', 'name')
    ordering_fields = ('product_code', 'name')
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
