# New file created
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from rest_framework.authtoken.models import Token

from apps.user.forms.banners_form import BannersForm, ResetPasswordForm
from apps.user.models import Banners, User
from lib.token_handler import token_expire_handler, is_token_expired


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


@method_decorator(csrf_exempt, name='dispatch')
class BannersDeleteView(DeleteView):
	queryset = Banners.objects.all()
	template_name = 'paper/user/banners_delete.html'
	model = Banners


