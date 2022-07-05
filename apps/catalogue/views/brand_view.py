# New file created
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework.permissions import BasePermission

from apps.catalogue.forms.brand_form import BrandForm
from apps.catalogue.models import Brand
from lib.permissions import IsAdmin


def issuperuser(request):
    from apps.user.models import Role
    return bool(request.user and request.user.is_superuser)


# @method_decorator(user_passes_test(issuperuser), name='dispatch')
class BrandDetailView(UpdateView, ListView):
    queryset = Brand.objects.all()
    template_name = 'paper/catalogue/brand_list.html'
    model = Brand
    form_class = BrandForm
    success_url = '/catalogue/brand/list/'
    extra_context = {
        "breadcrumbs": settings.BREAD.get('brand-list')
    }


class BrandListView(CreateView, ListView):
    queryset = Brand.objects.all()
    template_name = 'paper/catalogue/brand_list.html'
    model = Brand
    form_class = BrandForm
    success_url = '/catalogue/brand/list/'
    extra_context = {
        "breadcrumbs": settings.BREAD.get('brand-list')
    }

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.add_message(request, messages.INFO, form.errors.get('name')[0])
        return redirect('brand-list')


@method_decorator(csrf_exempt, name='dispatch')
class BrandDeleteView(DeleteView):
    queryset = Brand.objects.all()
    template_name = 'paper/catalogue/brand_list.html'
    model = Brand
    success_url = reverse_lazy('brand-list')

    # success_url = '/catalogue/brand/list/'

    def get(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        print(self.get_object().delete())
        return redirect('brand-list')

