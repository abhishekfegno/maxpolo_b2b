# New file created
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, DeleteView, ListView
from django.views.generic.edit import FormMixin
from django_filters.rest_framework import DjangoFilterBackend

from apps.catalogue.forms.product_form import ProductForm
from apps.catalogue.models import Product
from lib.filters import ProductFilter


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductDetailView(UpdateView, ListView):
    queryset = Product.objects.all().select_related('brand', 'category').order_by('-id')
    template_name = 'paper/catalogue/product_list.html'
    model = Product
    form_class = ProductForm
    filtering_backends = (DjangoFilterBackend,)
    filtering_class = ProductFilter
    success_url = '/catalogue/product/list/'
    extra_context = {
        "breadcrumbs": settings.BREAD.get('product-list')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        page_size = self.request.GET.get('page_size', 10)
        queryset = ProductFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = ProductFilter(self.request.GET, queryset=self.get_queryset()).form
        # import pdb;pdb.set_trace()
        paginator = Paginator(queryset.qs, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        filter = paginator.get_page(page_number)
        context['filter'] = filter
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductListView(FormMixin, ListView):
    queryset = Product.objects.all().select_related('brand', 'category').order_by('-id')
    template_name = 'paper/catalogue/product_list.html'
    model = Product
    form_class = ProductForm
    filtering_backends = (DjangoFilterBackend,)
    filtering_class = ProductFilter
    filterset_fields = ('name', 'product_code', 'brand')
    success_url = '/catalogue/product/list/'
    extra_context = {
        "breadcrumbs": settings.BREAD.get('product-list')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        page_size = self.request.GET.get('page_size', 10)
        queryset = ProductFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = ProductFilter(self.request.GET, queryset=self.get_queryset()).form
        # import pdb;pdb.set_trace()
        paginator = Paginator(queryset.qs, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        filter = paginator.get_page(page_number)
        context['filter'] = filter
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
            messages.add_message(request,messages.ERROR, form.errors)
        return redirect('product-list')


@method_decorator(csrf_exempt, name='dispatch')
class ProductDeleteView(DeleteView):
    queryset = Product.objects.all()
    template_name = 'paper/catalogue/product_list.html'
    model = Product
    success_url = '/catalogue/product/list/'


    def get(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        print(self.get_object().delete())
        return redirect('product-list')
