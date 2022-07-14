from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum, F, Count, Value
from django.db.models.functions import Concat
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
from apps.catalogue.models import Product, Brand, Category, PDF
from apps.order.models import SalesOrder, SalesOrderLine
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

        context['brand_count'] = Brand.objects.all().count()
        context['category_count'] = Category.objects.all().count()
        context['executives'] = User.objects.filter(user_role=Role.EXECUTIVE).count()
        context['dealers_count'] = User.objects.filter(user_role=Role.DEALER).count()
        context['pdf_catalogues'] = PDF.objects.all().count()
        context['net_credit'] = SalesOrder.objects.all().aggregate(total=Sum("invoice_remaining_amount"))['total']/100_000
        today = datetime.now().date()
        context['revenue_this_month'] = SalesOrder.objects.filter(created_at__year=today.year, created_at__month=today.month).aggregate(total=Sum(F("invoice_remaining_amount")))['total']/100_000

        context['advertisements'] = Banners.objects.all()

        # most purchased products
        context['products'] = SalesOrderLine.objects.all().annotate(name=F('product__name')).values('name').annotate(total=Sum('quantity')).order_by('-total')[:10]
        context['products'].maxval = max(context['products'], key=lambda a : a['total'])

        # most purchased brands
        context['brands'] = SalesOrderLine.objects.all().annotate(name=F('product__brand__name')).values('name').annotate(total=Sum('quantity')).order_by('-total')[:10]
        context['brands'].maxval = max(context['brands'], key=lambda a :a['total'])

        # most purchased categories
        context['categories'] = SalesOrderLine.objects.all().annotate(name=F('product__category__name')).values('name').annotate(total=Sum('quantity')).order_by('-total')[:10]
        context['categories'].maxval = max(context['categories'], key=lambda a :a['total'])

        # most purchased dealer quantity
        context['dealers'] = SalesOrder.objects.all().annotate(name=Concat(F('dealer__first_name'), Value(' '), F('dealer__last_name'))).values('name').annotate(total=Sum('line__quantity')).order_by('-total')[:10]
        context['dealers'].maxval = max(context['dealers'], key=lambda a :a['total'])

        # most purchased dealer amount
        context['amt_dealers'] = SalesOrder.objects.all().annotate(name=Concat(F('dealer__first_name'), Value(' '), F('dealer__last_name'))).values('name').annotate(total=Sum('invoice_amount')).order_by('-total')[:10]
        context['amt_dealers'].maxval = max(context['amt_dealers'], key=lambda a :a['total'])

        context['complaints'] = Complaint.objects.all().select_related('order_id').filter(status__in=['under processing', 'new']).order_by('-created_by')[:10]
        context['complaints_count'] = Complaint.objects.all().select_related('order_id').filter(status__in=['under processing', 'new']).count()

        context['pie_data'] = orders

        # oldest unpaid invoices
        context['unpaid_dealers'] = SalesOrder.objects.all().annotate(name=Concat(F('dealer__first_name'), Value(' '), F('dealer__last_name'))).values('name').filter(invoice_remaining_amount__lte=F('invoice_amount')).annotate(total=Sum('invoice_amount')).order_by('-total')[:10]
        context['unpaid_dealers'].maxval = max(context['unpaid_dealers'], key=lambda a :a['total'])

        # least moving products
        context['least_moving_products'] = SalesOrderLine.objects.all().annotate(name=F('product__name')).values('name').annotate(total=Sum('quantity')).order_by('total')[:10]
        context['least_moving_products'].maxval = max(context['least_moving_products'], key=lambda a :a['total'])

        # least moving products
        context['most_moving_products'] = SalesOrderLine.objects.all().annotate(name=F('product__name')).values('name').annotate(total=Sum('quantity')).order_by('-total')[:10]
        context['most_moving_products'].maxval = max(context['most_moving_products'], key=lambda a :a['total'])

        # most purchased executive volume
        context['executive_list'] = SalesOrder.objects.all().annotate(name=Concat(F('dealer__executive__first_name'), Value(' '), F('dealer__executive__last_name'))).values('name').annotate(total=Sum('invoice_amount')).order_by('-total')[:10]
        context['executive_list'].maxval = max(context['executive_list'], key=lambda a: a['total'])

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
                token.delete()
                token = Token.objects.create(user=token.user)

            user = User.objects.get(id=token.user.id)
            if form.is_valid():
                user.set_password(form.data.get('confirm_password'))
                user.save()
                # print(user.password)
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
