from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, UpdateView, ListView
from django.views.generic.edit import FormMixin

from apps.payment.forms import TransactionForm, TransactionUpdateForm
from apps.payment.models import Transaction
from lib.filters import PaymentFilter
from lib.importexport import PaymentReport


def get_excel_report_payment(request):
    queryset = Transaction.objects.select_related('order').order_by('created_at')
    name = 'payment'
    dataset = PaymentReport().export(queryset)
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{name}.xls"'
    return response


class TransactionDetailView(UpdateView, ListView):
    queryset = Transaction.objects.select_related('order').order_by('created_at')
    template_name = 'paper/payment/transaction_list.html'
    model = Transaction
    form_class = TransactionUpdateForm
    success_url = '/payment/transaction/list'


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                print(str(e))
                messages.add_message(request, messages.INFO, str(e))
        else:
            messages.add_message(request, messages.INFO, form.errors)
        return redirect('transaction-list')


class TransactionListView(FormMixin, ListView):
    queryset = Transaction.objects.select_related('order').order_by('created_at')
    template_name = 'paper/payment/transaction_list.html'
    model = Transaction
    form_class = TransactionForm
    success_url = '/payment/transaction/list'
    extra_context = {
        "breadcrumbs": settings.BREAD.get('transaction-list')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        page_size = self.request.GET.get('page_size', 10)
        queryset = PaymentFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = PaymentFilter(self.request.GET, queryset=self.get_queryset()).form
        # import pdb;pdb.set_trace()
        paginator = Paginator(queryset.qs, page_size)
        try:
            page_number = paginator.validate_number(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
        filter = paginator.get_page(page_number)
        context['filter'] = filter
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                print(str(e))
                messages.add_message(request, messages.INFO, str(e))
        else:
            messages.add_message(request, messages.INFO, form.errors)
        return redirect('transaction-list')


@method_decorator(csrf_exempt, name='dispatch')
class TransactionDeleteView(DeleteView):
    queryset = Transaction.objects.all().select_related('order')
    template_name = 'templates/transaction_list.html'
    model = Transaction
    success_url = '/payment/transaction/list'
