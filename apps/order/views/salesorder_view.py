# New file created
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from django.views.generic.edit import FormMixin
from django_filters.rest_framework import DjangoFilterBackend

from apps.catalogue.models import Product
from apps.order.forms.salesorder_form import QuotationForm, QuotationLineForm, QuotationUpdateForm, InvoiceUpdateForm, \
	SalesOrderUpdateForm
from apps.order.models import SalesOrder, SalesOrderLine
from lib.filters import OrderFilter
from lib.importexport import OrderReport


def get_orderline_form(request):
	form = QuotationLineForm
	return render(request, 'paper/line_form_htmx.html', context={'form': form})


def get_orderline(request, order_id):
	data = SalesOrderLine.objects.filter(order_id=order_id)
	return render(request, 'paper/order/order_line_list.html', context={'object_list': data})


def get_excel_report_order(request, slug):
	queryset = SalesOrder.objects.filter(is_quotation=True)
	name = 'quotation'
	if slug.lower() == 'salesorder':
		queryset = SalesOrder.objects.filter(is_confirmed=True)
		name = slug
	if slug.lower() == 'invoice':
		queryset = SalesOrder.objects.filter(is_invoice=True)
		name = slug
	dataset = OrderReport().export(queryset)
	response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = f'attachment; filename="{name}.xls"'
	return response


def cancelled_order(request):
	queryset = SalesOrder.objects.all().filter(is_cancelled=True).select_related('dealer')
	context = {}
	context['filter'] = OrderFilter(request.GET, queryset=queryset)
	context['order_type'] = 'Cancelled'
	return render(request, 'paper/order/cancelled_order_list.html', context=context)


class SalesOrderDetailView(UpdateView):
	queryset = SalesOrder.objects.all().filter(is_confirmed=True).select_related('dealer')
	template_name = 'paper/order/salesorder_form.html'
	model = SalesOrder
	form_class = SalesOrderUpdateForm
	success_url = '/order/order/list'


class SalesOrderListView(FormMixin, ListView):
	queryset = SalesOrder.objects.all().filter(is_confirmed=True, is_invoice=False).select_related('dealer')
	template_name = 'paper/order/salesorder_list.html'
	model = SalesOrder
	form_class = QuotationForm
	filtering_backends = (DjangoFilterBackend,)
	filtering_class = OrderFilter
	filterset_fields = ('order_id',)
	success_url = '/order/order/list'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['orderform'] = QuotationForm
		context['orderlineform'] = QuotationLineForm
		context['order_type'] = 'SalesOrder'
		context['filter'] = OrderFilter(self.request.GET, queryset=self.get_queryset())
		page_number = self.request.GET.get('page', 1)
		page_size = self.request.GET.get('page_size', 10)
		queryset = OrderFilter(self.request.GET, queryset=self.get_queryset())
		context['filter_form'] = OrderFilter(self.request.GET, queryset=self.get_queryset()).form
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
	queryset = SalesOrder.objects.all().select_related('dealer')
	template_name = 'templates/salesorder_list.html'
	model = SalesOrder
	success_url = '/order/order/list'


class QuotationDetailView(UpdateView):
	queryset = SalesOrder.objects.all().filter(is_quotation=True).select_related('dealer')
	template_name = 'paper/order/salesorder_form.html'
	model = SalesOrder
	form_class = QuotationUpdateForm
	success_url = '/order/quotation/list'


class QuotationListView(FormMixin, ListView):
	queryset = SalesOrder.objects.all().filter(is_quotation=True, is_cancelled=False, is_confirmed=False, is_invoice=False).select_related('dealer')
	template_name = 'paper/order/quotation_list.html'
	model = SalesOrder
	form_class = QuotationForm
	filtering_backends = (DjangoFilterBackend, )
	filtering_class = OrderFilter
	filterset_fields = ('order_id',)
	success_url = '/order/quotation/list'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['orderform'] = QuotationForm
		context['orderlineform'] = QuotationLineForm
		context['order_type'] = 'Quotation'
		page_number = self.request.GET.get('page', 1)
		page_size = self.request.GET.get('page_size', 10)
		queryset = OrderFilter(self.request.GET, queryset=self.get_queryset())
		context['filter_form'] = OrderFilter(self.request.GET, queryset=self.get_queryset()).form
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
		form = QuotationForm(request.POST)
		if form.is_valid():
			products = form.data.get('product')
			quantity = form.data.get('quantity')
			order = form.save()
			for product, quantity in zip(products, quantity):
				line = SalesOrderLine.objects.create(product=Product.objects.get(id=product), quantity=quantity, order=order)
				print(f"line created {line} for order {order}")
		else:
			messages.add_message(request, messages.INFO, form.errors)
		return redirect('quotation-list')


@method_decorator(csrf_exempt, name='dispatch')
class QuotationDeleteView(DeleteView):
	queryset = SalesOrder.objects.all().select_related('dealer')
	template_name = 'templates/quotation_list.html'
	model = SalesOrder
	success_url = '/order/quotation/list'


class InvoiceDetailView(UpdateView):
	queryset = SalesOrder.objects.all().filter(is_invoice=True).select_related('dealer')
	template_name = 'paper/order/invoice_form.html'
	model = SalesOrder
	form_class = InvoiceUpdateForm
	success_url = '/order/invoice/list'


class InvoiceListView(FormMixin, ListView):
	queryset = SalesOrder.objects.all().filter(is_invoice=True).select_related('dealer')
	template_name = 'paper/order/invoice_list.html'
	model = SalesOrder
	form_class = InvoiceUpdateForm
	filtering_backends = (DjangoFilterBackend,)
	filtering_class = OrderFilter
	filterset_fields = ('order_id',)
	success_url = '/order/invoice/list'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['orderform'] = QuotationForm
		context['orderlineform'] = QuotationLineForm
		context['order_type'] = 'Invoice'
		context['filter'] = OrderFilter(self.request.GET, queryset=self.get_queryset())
		page_number = self.request.GET.get('page', 1)
		page_size = self.request.GET.get('page_size', 10)
		queryset = OrderFilter(self.request.GET, queryset=self.get_queryset())
		context['filter_form'] = OrderFilter(self.request.GET, queryset=self.get_queryset()).form
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
		form = InvoiceUpdateForm(request.POST)
		if form.is_valid():
			products = form.data.get('product')
			quantity = form.data.get('quantity')
			order = form.save()
			for product, quantity in zip(products, quantity):
				line = SalesOrderLine.objects.create(product=Product.objects.get(id=product), quantity=quantity, order=order)
				print(f"line created {line} for order {order}")
		return redirect('invoice-list')


@method_decorator(csrf_exempt, name='dispatch')
class InvoiceDeleteView(DeleteView):
	queryset = SalesOrder.objects.all().select_related('dealer')
	template_name = 'templates/invoice_list.html'
	model = SalesOrder
	success_url = '/order/invoice/list'



