from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework.reverse import reverse

from apps.user.forms.banners_form import BannersForm
from apps.user.models import Banners
from lib.sent_email import EmailHandler


class BannersDetailView(UpdateView):
    queryset = Banners.objects.all()
    template_name = 'paper/user/banners_form.html'
    model = Banners
    form_class = BannersForm
    success_url = '/banners/list/'


class BannersListView(SuccessMessageMixin, CreateView, ListView):
    queryset = Banners.objects.all()
    template_name = 'paper/user/banners_list.html'
    model = Banners
    form_class = BannersForm
    success_url = '/banners/list/'
    extra_context = {
        "breadcrumbs": settings.BREAD.get('banners-list')
    }
    success_message = 'Banner'

    def post(self, request, *args, **kwargs):
        url = reverse('banners-list', request=request, format=None)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            EmailHandler().sent_mail_for_banners(instance, url)
        else:
            print(form.errors)
            messages.add_message(request, messages.INFO, form.errors.get('file')[0])
        return redirect('banners-list')


@method_decorator(csrf_exempt, name='dispatch')
class BannersDeleteView(DeleteView):
    queryset = Banners.objects.all()
    template_name = 'paper/user/banners_delete.html'
    model = Banners
    success_url = '/banners/list/'
