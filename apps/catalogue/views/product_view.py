# New file created 
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.catalogue.forms.product_form import ProductForm
from apps.catalogue.models import Product


class ProductDetailView(DetailView):
	queryset = Product.objects.all()
	template_name = 'templates/product_detail.html'
	model = Product


class ProductListView(CreateView, ListView):
	queryset = Product.objects.all()
	template_name = 'paper/catalogue/product_list.html'
	model = Product
	form_class = ProductForm


class ProductDeleteView(DeleteView):
	queryset = Product.objects.all()
	template_name = 'templates/product_delete.html'
	model = Product


