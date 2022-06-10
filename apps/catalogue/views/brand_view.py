# New file created 
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.catalogue.forms.brand_form import BrandForm
from apps.catalogue.models import Brand


class BrandDetailView(DetailView):
	queryset = Brand.objects.all()
	template_name = 'paper/catalogue/brand_detail.html'
	model = Brand


class BrandListView(CreateView, ListView):
	queryset = Brand.objects.all()
	template_name = 'paper/catalogue/brand_list.html'
	model = Brand
	form_class = BrandForm


class BrandDeleteView(DeleteView):
	queryset = Brand.objects.all()
	template_name = 'paper/catalogue/brand_delete.html'
	model = Brand


