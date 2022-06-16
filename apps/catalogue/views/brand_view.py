# New file created
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.catalogue.forms.brand_form import BrandForm
from apps.catalogue.models import Brand


class BrandDetailView(UpdateView):
	queryset = Brand.objects.all()
	template_name = 'paper/catalogue/brand_form.html'
	model = Brand
	form_class = BrandForm
	success_url = '/catalogue/brand/list/'


class BrandListView(CreateView, ListView):
	queryset = Brand.objects.all()
	template_name = 'paper/catalogue/brand_list.html'
	model = Brand
	form_class = BrandForm
	success_url = '/catalogue/brand/list/'


@method_decorator(csrf_exempt, name='dispatch')
class BrandDeleteView(DeleteView):
	queryset = Brand.objects.all()
	template_name = 'paper/catalogue/brand_list.html'
	model = Brand
	success_url = reverse_lazy('brand-list')

	# success_url = '/catalogue/brand/list/'

	def post(self, request, *args, **kwargs):
		"""
		Call the delete() method on the fetched object and then redirect to the
		success URL.
		"""
		self.object = self.get_object()
		success_url = self.get_success_url()
		# import pdb;pdb.set_trace()
		self.object.delete()
		return HttpResponseRedirect(success_url)



