# New file created
from django.shortcuts import render
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


class BannersDeleteView(DeleteView):
	queryset = Banners.objects.all()
	template_name = 'paper/user/banners_delete.html'
	model = Banners


def password_reset(request, token):
	errors = ""
	form = ResetPasswordForm(request.POST)

	if request.method == 'POST':
		try:
			token = Token.objects.get(key=token)
			if is_token_expired(token):
				return render(request, 'registration/password_reset_confirm.html', context={'errors': errors})
			token = token_expire_handler(token)

			user = User.objects.get(id=token.user.id)
			if form.is_valid():
				user.set_password(form.data.get('confirm_password'))
				user.save()
				print(user.password)
				return render(request, 'registration/password_reset_complete.html')
		except Exception as e:
			errors = str(e)

	return render(request, 'registration/password_reset_confirm.html', context={'form': form, 'errors': errors})
