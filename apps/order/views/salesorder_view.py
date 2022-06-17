# New file created
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from django.views.generic.edit import FormMixin

from apps.catalogue.models import Product
from apps.order.forms.salesorder_form import QuotationForm, QuotationLineForm, QuotationUpdateForm
from apps.order.models import SalesOrder, SalesOrderLine


def get_orderline_form(request):
	form = QuotationLineForm
	return render(request, 'paper/line_form_htmx.html',context={'form':form})


class SalesOrderDetailView(UpdateView):
	queryset = SalesOrder.objects.all()
	template_name = 'paper/order/salesorder_form.html'
	model = SalesOrder
	form_class = QuotationUpdateForm
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
		context['order_type'] = 'Quotation'
		return context

	def post(self, request, *args, **kwargs):
		form = QuotationForm(request.POST)
		if form.is_valid():
			products = form.data.get('product')
			quantity = form.data.get('quantity')
			order = form.save()
			for product, quantity in zip(products, quantity):
				line = SalesOrderLine.objects.create(product=Product.objects.get(id=product), quantity=quantity, order=order)
				print(f"line created {line} for order {order}")
		return redirect('salesorder-list')


@method_decorator(csrf_exempt, name='dispatch')
class SalesOrderDeleteView(DeleteView):
	queryset = SalesOrder.objects.all()
	template_name = 'templates/salesorder_list.html'
	model = SalesOrder
	success_url = '/order/order/list/'



