from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, UpdateView, ListView
from django.views.generic.edit import FormMixin

from apps.payment.forms import TransactionForm
from apps.payment.models import Transaction


class TransactionDetailView(UpdateView):
    queryset = Transaction.objects.select_related('order')
    template_name = 'paper/payment/salesorder_form.html'
    model = Transaction
    form_class = TransactionForm
    success_url = '/payment/transaction/list'


class TransactionListView(FormMixin, ListView):
    queryset = Transaction.objects.select_related('order')
    template_name = 'paper/payment/transaction_list.html'
    model = Transaction
    form_class = TransactionForm
    success_url = '/payment/transaction/list'

# def get_context_data(self, **kwargs):
# 	context = super().get_context_data(**kwargs)
# 	context['orderform'] = QuotationForm
# 	context['orderlineform'] = QuotationLineForm
# 	context['order_type'] = 'SalesOrder'
# 	return context


@method_decorator(csrf_exempt, name='dispatch')
class TransactionDeleteView(DeleteView):
    queryset = Transaction.objects.all().select_related('order')
    template_name = 'templates/transaction_list.html'
    model = Transaction
    success_url = '/payment/transaction/list'
