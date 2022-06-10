# New file created 
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.catalogue.forms.category_form import CategoryForm
from apps.catalogue.models import Category


class CategoryCreateView(CreateView):
	queryset = Category.objects.all()
	template_name = 'paper/catalogue/category_create.html'
	model = Category
	form_class = CategoryForm


class CategoryDetailView(DetailView):
	queryset = Category.objects.all()
	template_name = 'paper/catalogue/category_detail.html'
	model = Category


class CategoryListView(CreateView, ListView):
	queryset = Category.objects.all()
	template_name = 'paper/catalogue/category_list.html'
	model = Category
	form_class = CategoryForm


class CategoryDeleteView(DeleteView):
	queryset = Category.objects.all()
	template_name = 'paper/catalogue/category_delete.html'
	model = Category


