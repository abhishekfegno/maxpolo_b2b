# New file created
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from django.views.generic.edit import FormMixin

from apps.order.forms.salesorder_form import QuotationForm, QuotationLineForm
from apps.order.models import SalesOrder


def get_orderline_form(request):
	form = QuotationLineForm
	return render(request, 'paper/line_form_htmx.html',context={'form':form})


class SalesOrderDetailView(UpdateView):
	queryset = SalesOrder.objects.all()
	template_name = 'paper/order/salesorder_form.html'
	model = SalesOrder
	form_class = QuotationForm
	success_url = '/order/order/list/'


class SalesOrderListView(FormMixin, ListView):
	queryset = SalesOrder.objects.all()
	template_name = 'paper/order/salesorder_list.html'
	model = SalesOrder
	form_class = QuotationForm
	success_url = '/order/order/list/'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['orderform'] = QuotationForm
		context['orderlineform'] = QuotationLineForm
		return context

	def post(self, request, *args, **kwargs):
		form1 = QuotationForm(request.POST)
		form2 = QuotationLineForm(request.POST)
		if form1.is_valid() and form2.is_valid():
			form1.save()
			form2.save()
		return redirect('salesorders-list')


@method_decorator(csrf_exempt, name='dispatch')
class SalesOrderDeleteView(DeleteView):
	queryset = SalesOrder.objects.all()
	template_name = 'templates/salesorder_list.html'
	model = SalesOrder
	success_url = '/order/order/list/'



