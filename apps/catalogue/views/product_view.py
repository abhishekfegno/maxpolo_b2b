# New file created
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from django.views.generic.edit import ProcessFormView, ModelFormMixin, FormMixin
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.views import FilterView

from apps.catalogue.forms.product_form import ProductForm
from apps.catalogue.models import Product
from lib.filters import ProductFilter


class ProductDetailView(UpdateView):
	queryset = Product.objects.all()
	template_name = 'paper/catalogue/product_form.html'
	model = Product
	form_class = ProductForm
	success_url = '/catalogue/product/list/'


class ProductListView(FormMixin, ListView):
	queryset = Product.objects.all().select_related('brand', 'category')
	template_name = 'paper/catalogue/product_list.html'
	model = Product
	form_class = ProductForm
	filtering_backends = (DjangoFilterBackend, )
	filtering_class = ProductFilter
	filterset_fields = ('name', 'product_code', 'brand')
	success_url = '/catalogue/product/list/'

	def get_context_data(self, **kwargs):
		cxt = super().get_context_data(**kwargs)
		cxt['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
		return cxt

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			form.save()
		else:
			print(form.errors)
		return redirect('product-list')


@method_decorator(csrf_exempt, name='dispatch')
class ProductDeleteView(DeleteView):
	queryset = Product.objects.all()
	template_name = 'paper/catalogue/product_list.html'
	model = Product
	success_url = '/catalogue/product/list/'


