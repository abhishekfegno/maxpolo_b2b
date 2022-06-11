# New file created 
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.user.forms.banners_form import BannersForm
from apps.user.models import Banners


class BannersDetailView(UpdateView):
	queryset = Banners.objects.all()
	template_name = 'paper/user/banners_form.html'
	model = Banners
	form_class = BannersForm
	success_url = '/banners/list/'


class BannersListView(CreateView, ListView):
	queryset = Banners.objects.all()
	template_name = 'paper/user/banners_list.html'
	model = Banners
	form_class = BannersForm
	success_url = '/banners/list/'


class BannersDeleteView(DeleteView):
	queryset = Banners.objects.all()
	template_name = 'paper/user/banners_delete.html'
	model = Banners


