from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework.reverse import reverse

from apps.user.forms.banners_form import *
from apps.user.models import Banners
from lib.sent_email import EmailHandler


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class BannersDetailView(UpdateView, ListView):
	queryset = Banners.objects.all().filter(user_type='dealer')
	template_name = 'paper/user/banners_list.html'
	model = Banners
	form_class = DealerBannersForm
	success_url = 'banners/list/'

	def post(self, request, *args, **kwargs):
		# url = reverse('banners-list', request=request, format=None)
		form = self.form_class(request.POST, request.FILES, instance=self.get_object())
		if form.is_valid():
			instance = form.save()
		else:
			print(form.errors)
			# import pdb;pdb.set_trace()
			messages.add_message(request, messages.ERROR, form.errors.get('file')[0])
		return redirect('banners-list')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class BannersListView(CreateView, ListView):
	queryset = Banners.objects.all()
	template_name = 'paper/user/banners_list.html'
	model = Banners
	form_class = DealerBannersForm

	success_url = 'banners/list/'
	extra_context = {
		"breadcrumbs": settings.BREAD.get('banners-list')
	}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['type'] = 'Dealer'
		queryset = self.get_queryset().filter(user_type='dealer')
		page_number = self.request.GET.get('page', 1)
		page_size = self.request.GET.get('page_size', 10)
		paginator = Paginator(queryset, page_size)
		try:
			page_number = paginator.validate_number(page_number)
		except EmptyPage:
			page_number = paginator.num_pages
		filter = paginator.get_page(page_number)
		context['object_list'] = filter
		context['filter'] = filter
		return context

	def post(self, request, *args, **kwargs):
		# url = reverse('banners-list', request=request, format=None)
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user_type = 'dealer'
			instance.save()
		else:
			print(form.errors)
			# import pdb;pdb.set_trace()
			messages.add_message(request, messages.ERROR, form.errors.get('file')[0])
		return redirect('banners-list')


@method_decorator(csrf_exempt, name='dispatch')
class BannersDeleteView(DeleteView):
	queryset = Banners.objects.all()
	template_name = 'paper/user/banners_delete.html'
	model = Banners
	success_url = 'banners/list/'

	def post(self, request, *args, **kwargs):
		# import pdb;pdb.set_trace()
		print(self.get_object().delete())
		return redirect('banners-list')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ExecutiveBannersDetailView(UpdateView, ListView):
	queryset = Banners.objects.all().filter(user_type='executive')
	template_name = 'paper/user/executive_banners_list.html'
	model = Banners
	form_class = ExecutiveBannersForm
	success_url = 'banners/executive/list/'

	def post(self, request, *args, **kwargs):
		# url = reverse('banners-list', request=request, format=None)
		form = self.form_class(request.POST, request.FILES, instance=self.get_object())
		if form.is_valid():
			instance = form.save()
		else:
			print(form.errors)
			# import pdb;pdb.set_trace()
			messages.add_message(request, messages.ERROR, form.errors.get('file')[0])
		return redirect('executive-banners-list')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ExecutiveBannersListView(CreateView, ListView):
	queryset = Banners.objects.all()
	template_name = 'paper/user/executive_banners_list.html'
	model = Banners
	form_class = ExecutiveBannersForm

	success_url = 'banners/executive/list/'
	extra_context = {
		"breadcrumbs": settings.BREAD.get('banners-list')
	}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['type'] = 'Executive'
		queryset = self.get_queryset().filter(user_type='executive')
		context['object_list'] = queryset
		page_number = self.request.GET.get('page', 1)
		page_size = self.request.GET.get('page_size', 10)
		paginator = Paginator(queryset, page_size)
		try:
			page_number = paginator.validate_number(page_number)
		except EmptyPage:
			page_number = paginator.num_pages
		filter = paginator.get_page(page_number)
		context['object_list'] = filter
		context['filter'] = filter
		return context


	def post(self, request, *args, **kwargs):
		# url = reverse('banners-list', request=request, format=None)
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user_type = 'executive'
			instance.save()
		else:
			print(form.errors)
			# import pdb;pdb.set_trace()
			messages.add_message(request, messages.ERROR, form.errors.get('file')[0])
		return redirect('executive-banners-list')


@method_decorator(csrf_exempt, name='dispatch')
class ExecutiveBannersDeleteView(DeleteView):
	queryset = Banners.objects.all()
	template_name = 'paper/user/banners_delete.html'
	model = Banners
	success_url = 'banners/executive/list/'

	def post(self, request, *args, **kwargs):
		# import pdb;pdb.set_trace()
		print(self.get_object().delete())
		return redirect('executive-banners-list')
