# New file created
import os

from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.edit import ProcessFormView, ModelFormMixin
from rest_framework.reverse import reverse

from apps.catalogue.forms.category_form import CategoryForm, PDFForm
from apps.catalogue.models import Category, PDF
from lib.sent_email import EmailHandler


class CategoryListView(ModelFormMixin, ListView, ProcessFormView):
    queryset = Category.get_root_nodes()
    template_name = 'paper/catalogue/category_list.html'
    model = Category
    form_class = CategoryForm
    success_url = '/catalogue/category/list/'
    allow_empty = True
    extra_context = {
        "breadcrumbs": settings.BREAD.get('category-list')
    }

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super(CategoryListView, self).get_object(queryset=Category.objects.all())
        return None

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.object = self.get_object(self.object_list)
        allow_empty = self.get_allow_empty()
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
            Handle POST requests: instantiate a form instance with the passed
            POST variables and then check if it's valid.
		"""
        form = self.get_form()
        if form.is_valid():
            form.save()
        else:
            messages.add_message(request, messages.INFO, form.errors.get('name')[0])
        return redirect('category-list')


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    queryset = Category.objects.all()
    template_name = 'paper/catalogue/category_delete.html'
    model = Category
    success_url = '/catalogue/category/list/'

    def get(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        print(self.get_object().delete())
        return redirect('category-list')


class PDFListView(UpdateView, ListView):
    queryset = PDF.objects.all()
    template_name = 'paper/catalogue/pdf_list.html'
    model = PDF
    form_class = PDFForm
    success_url = '/catalogue/pdf/list/'
    extra_context = {
        "breadcrumbs": settings.BREAD.get('pdf-list')
    }

    def get_object(self, queryset=None):
        if len(self.kwargs.keys()):
            return super(PDFListView, self).get_object(queryset)
        return None

    def post(self, request, *args, **kwargs):
        url = reverse('pdf-list', request=request, format=None, )
        form = self.form_class(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            instance = form.save()
            # EmailHandler().sent_mail_for_pdf(instance, url)
        else:
            print(form.errors)
            messages.add_message(request, messages.ERROR, form.errors.get('file')[0])
        return redirect('pdf-list')


class PDFDetailView(UpdateView):
    queryset = PDF.objects.all()
    template_name = 'paper/catalogue/pdf_form.html'
    model = PDF
    form_class = PDFForm
    success_url = '/catalogue/pdf/list/'

    def get(self, request, *args, **kwargs):
        objkey = self.kwargs.get('pk', None)  # 1
        try:
            pdf = get_object_or_404(PDF, pk=objkey)  # 2
            fname = pdf.filename()  # 3
            # import pdb;pdb.set_trace()

            path = os.path.join(settings.MEDIA_ROOT, 'pdf/product/' + fname)  # 4
            response = FileResponse(open(path, 'rb'), content_type="application/pdf")
            response["Content-Disposition"] = "filename={}".format(fname)
        except Exception as e:
            print(str(e))
            response = HttpResponse()
            response['errors'] = str(e)
        return response


@method_decorator(csrf_exempt, name='dispatch')
class PDFDeleteView(DeleteView):
    queryset = PDF.objects.all()
    template_name = 'paper/catalogue/pdf_list.html'
    model = PDF
    success_url = '/catalogue/pdf/list/'
