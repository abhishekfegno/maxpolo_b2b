# New file created
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.order.forms.salesorder_form import QuotationForm
from apps.order.models import SalesOrder


class SalesOrderDetailView(UpdateView):
	queryset = SalesOrder.objects.all()
	template_name = 'paper/order/salesorder_form.html'
	model = SalesOrder
	form_class = QuotationForm
	success_url = '/order/order/list/'


class SalesOrderListView(CreateView, ListView):
	queryset = SalesOrder.objects.all()
	template_name = 'paper/order/salesorder_list.html'
	model = SalesOrder
	form_class = QuotationForm
	success_url = '/order/order/list/'


@method_decorator(csrf_exempt, name='dispatch')
class SalesOrderDeleteView(DeleteView):
	queryset = SalesOrder.objects.all()
	template_name = 'templates/salesorder_list.html'
	model = SalesOrder
	success_url = '/order/order/list/'



