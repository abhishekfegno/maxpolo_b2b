from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, DeleteView, ListView, TemplateView
from django.views.generic.edit import FormMixin, ModelFormMixin, ProcessFormView, FormView, CreateView
from rest_framework.authtoken.models import Token

from apps.executivetracking.models import Zone
from apps.user.forms.banners_form import DealerUpdateForm, ExecutiveUpdateForm, AdminUpdateForm, UserCreationForm, \
    ZoneForm
from apps.catalogue.models import Product, Brand
from apps.order.models import SalesOrder
from apps.user.forms.banners_form import ResetPasswordForm, DealerForm, ExecutiveForm, AdminForm
from apps.user.models import Banners, User, Dealer, Executive, Role, Complaint
from lib.token_handler import token_expire_handler, is_token_expired


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class IndexView(TemplateView):
    template_name = 'paper/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        quotation = SalesOrder.objects.filter(is_quotation=True).select_related('dealer')
        salesorder = SalesOrder.objects.filter(is_confirmed=True).select_related('dealer')
        invoice = SalesOrder.objects.filter(is_invoice=True).select_related('dealer')
        orders = {}
        orders['orders'] = quotation.count()
        orders['saleorder'] = salesorder.count()
        orders['invoice'] = invoice.count()

        context['orders'] = quotation
        context['salesorders'] = salesorder
        context['invoice'] = invoice

        context['advertisements'] = Banners.objects.all()
        context['products'] = Product.objects.all().select_related('brand', 'category')
        context['brands'] = Brand.objects.all()
        context['complaints'] = Complaint.objects.all().select_related('created_by', 'order_id')
        context['pie_data'] = orders
        print(orders)
        return self.render_to_response(context)


class UserDetailView(UpdateView):
    queryset = User.objects.all()
    form_class = UserCreationForm
    template_name = 'paper/user/user_list.html'
    model = User
    success_url = '/user/list/'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
        else:
            print(form.errors)
        role = form.instance.user_role
        return redirect('user-list', role=role)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserListView(ModelFormMixin, SuccessMessageMixin, ListView, ProcessFormView):
    queryset = User.objects.all()
    template_name = 'paper/user/user_list.html'
    home_label = _("User list")
    model = User
    form_class = DealerForm
    extra_context = {
        "breadcrumbs": settings.BREAD.get('user-list')
    }
    success_url = ''

    def get_template_names(self):
        if self.object:
            return 'paper/user/user_list_update.html'
        return self.template_name

    def get_success_message(self, cleaned_data):
        return f"{self.kwargs.get('role', '').capitalize()} has been Saved!"

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        if self.kwargs.get('role') == 'dealer':
            queryset = Dealer.objects.all().filter(user_role=Role.DEALER)
        if self.kwargs.get('role') == 'executive':
            queryset = Executive.objects.all().filter(user_role=Role.EXECUTIVE)
        if self.kwargs.get('role') == 'admin':
            queryset = User.objects.all().filter(user_role=Role.ADMIN)
        return queryset

    def get_form_class(self):
        if self.kwargs.get('role') == 'dealer':
            if self.object:
                return DealerUpdateForm
            return DealerForm
        if self.kwargs.get('role') == 'admin':
            if self.object:
                return AdminUpdateForm
            return AdminForm
        if self.kwargs.get('role') == 'executive':
            if self.object:
                return ExecutiveUpdateForm
            return ExecutiveForm
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.kwargs.get('role', '').capitalize()
        return context

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super(UserListView, self).get_object(queryset)
        return None

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.object = self.get_object()
        return super(UserListView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.object = self.get_object()
        return super(UserListView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('user-list', kwargs={'role': self.kwargs['role']})


class UserPasswordView(UpdateView):
    form_class = ResetPasswordForm
    queryset = User.objects.all()
    template_name = 'paper/user/user_password.html'
    home_label = "User Password Change"
    model = User
    extra_context = {
        "breadcrumbs": settings.BREAD.get('user-password')
    }
    pk_url_kwarg = 'pk'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        if self.kwargs.get('role') == 'dealer':
            queryset = Dealer.objects.all()
        if self.kwargs.get('role') == 'executive':
            queryset = Executive.objects.all()
        if self.kwargs.get('role') == 'admin':
            queryset = User.objects.all().filter(user_role=Role.ADMIN)
        return queryset

    def form_valid(self, form):
        self.object.set_password(form.cleaned_data['new_password'])
        self.object.save()
        return super(UserPasswordView, self).form_valid(form)

    def get_success_url(self):
        return reverse('user-update', kwargs=self.kwargs)


class UserDeleteView(DeleteView):
    queryset = User.objects.all()
    template_name = 'paper/user/user_list.html'
    model = User
    success_url = '/user/list/'


def password_reset(request, token):
    errors = ""
    form = ResetPasswordForm(request.POST or None)

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
            print(str(e))
    return render(request, 'registration/password_reset_confirm.html', context={'form': form, 'errors': errors})



class ZoneView(CreateView, ListView):
    queryset = Zone.objects.all()
    template_name = 'paper/user/zone_list.html'
    model = User
    form_class = ZoneForm
    success_url = '/zone/list/'


class ZoneUpdateView(UpdateView):
    queryset = Zone.objects.all()
    template_name = 'paper/user/zone_list.html'
    model = User
    form_class = ZoneForm
    success_url = '/zone/list/'


class ZoneDeleteView(DeleteView):
    queryset = Zone.objects.all()
    template_name = 'paper/user/zone_list.html'
    model = User
    form_class = ZoneForm
    success_url = '/zone/list/'
