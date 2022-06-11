# New file created 
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.catalogue.forms.category_form import CategoryForm
from apps.catalogue.models import Category


class CategoryDetailView(UpdateView):
	queryset = Category.objects.all()
	template_name = 'paper/catalogue/category_form.html'
	model = Category
	form_class = CategoryForm
	success_url = '/catalogue/category/list/'


class CategoryListView(CreateView, ListView):
	queryset = Category.objects.all()
	template_name = 'paper/catalogue/category_list.html'
	model = Category
	form_class = CategoryForm
	success_url = '/catalogue/category/list/'


class CategoryDeleteView(DeleteView):
	queryset = Category.objects.all()
	template_name = 'paper/catalogue/category_delete.html'
	model = Category
	success_url = '/catalogue/category/list/'


