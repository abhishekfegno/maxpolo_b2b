# New file created
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.catalogue.forms.product_form import ProductForm
from apps.catalogue.models import Product


class ProductDetailView(UpdateView):
	queryset = Product.objects.all()
	template_name = 'paper/catalogue/product_form.html'
	model = Product
	form_class = ProductForm
	success_url = '/catalogue/product/list/'


class ProductListView(CreateView, ListView):
	queryset = Product.objects.all()
	template_name = 'paper/catalogue/product_list.html'
	model = Product
	form_class = ProductForm
	success_url = '/catalogue/product/list/'


@method_decorator(csrf_exempt, name='dispatch')
class ProductDeleteView(DeleteView):
	queryset = Product.objects.all()
	template_name = 'paper/catalogue/product_delete.html'
	model = Product
	success_url = '/catalogue/product/list/'


