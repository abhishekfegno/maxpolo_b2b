# New file created
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.reverse import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from rest_framework.authtoken.models import Token

from apps.user.forms.banners_form import BannersForm, ResetPasswordForm
from apps.user.models import Banners, User
from lib.sent_email import EmailHandler
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

	def post(self, request, *args, **kwargs):
		url = reverse('banners-list', request=request, format=None)
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save()
			EmailHandler().sent_mail_for_banners(instance, url)
		else:
			print(form.errors)
			# import pdb;pdb.set_trace()
			messages.add_message(request, messages.INFO, form.errors.get('file')[0])
		return redirect('banners-list')


@method_decorator(csrf_exempt, name='dispatch')
class BannersDeleteView(DeleteView):
	queryset = Banners.objects.all()
	template_name = 'paper/user/banners_delete.html'
	model = Banners


