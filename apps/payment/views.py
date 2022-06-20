from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, UpdateView, ListView
from django.views.generic.edit import FormMixin

from apps.payment.forms import TransactionForm
from apps.payment.models import Transaction
from lib.importexport import PaymentReport


def get_excel_report_payment(request):
    queryset = Transaction.objects.select_related('order')
    name = 'payment'
    dataset = PaymentReport().export(queryset)
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{name}.xls"'
    return response


class TransactionDetailView(UpdateView):
    queryset = Transaction.objects.select_related('order')
    template_name = 'paper/payment/transaction_form.html'
    model = Transaction
    form_class = TransactionForm
    success_url = '/payment/transaction/list'


class TransactionListView(FormMixin, ListView):
    queryset = Transaction.objects.select_related('order')
    template_name = 'paper/payment/transaction_list.html'
    model = Transaction
    form_class = TransactionForm
    success_url = '/payment/transaction/list'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect('transaction-list')


@method_decorator(csrf_exempt, name='dispatch')
class TransactionDeleteView(DeleteView):
    queryset = Transaction.objects.all().select_related('order')
    template_name = 'templates/transaction_list.html'
    model = Transaction
    success_url = '/payment/transaction/list'
