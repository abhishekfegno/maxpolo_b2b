# New file created
import os

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.catalogue.forms.category_form import CategoryForm, PDFForm
from apps.catalogue.models import Category, PDF


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


class PDFListView(CreateView, ListView):
	queryset = PDF.objects.all()
	template_name = 'paper/catalogue/pdf_list.html'
	model = PDF
	form_class = PDFForm
	success_url = '/catalogue/pdf/list/'


class PDFDetailView(UpdateView):
	queryset = PDF.objects.all()
	template_name = 'paper/catalogue/pdf_form.html'
	model = PDF
	form_class = PDFForm
	success_url = '/catalogue/pdf/list/'

	def get(self, request, *args, **kwargs):
		objkey = self.kwargs.get('pk', None)  # 1
		pdf = get_object_or_404(PDF, pk=objkey)  # 2
		fname = pdf.filename()  # 3
		path = os.path.join(settings.MEDIA_ROOT, 'pdf/product/' + fname)  # 4
		response = FileResponse(open(path, 'rb'), content_type="application/pdf")
		response["Content-Disposition"] = "filename={}".format(fname)
		return response