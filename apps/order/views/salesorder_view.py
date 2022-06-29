# New file created
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from django.views.generic.edit import FormMixin
from django_filters.rest_framework import DjangoFilterBackend

from apps.catalogue.models import Product
from apps.order.forms.salesorder_form import QuotationForm, QuotationLineForm, QuotationUpdateForm, InvoiceUpdateForm, \
	SalesOrderUpdateForm, InvoiceAmountForm
from apps.order.models import SalesOrder, SalesOrderLine
from apps.payment.models import QuantityInvalidException
from lib.filters import OrderFilter
from lib.importexport import OrderReport


def get_orderline_form(request):
	form = QuotationLineForm
	return render(request, 'paper/line_form_htmx.html', context={'form': form})


def form_submit(request, order):
	if order.order_type == 'quotation':
		form = QuotationUpdateForm(request.POST or None, instance=order)
	else:
		form = SalesOrderUpdateForm(request.POST or None, instance=order)
	return form


def get_orderline(request, order_id):
	context = {}
	order = SalesOrder.objects.get(id=order_id)
	form = form_submit(request, order)
	context['del'] = order.order_type + '-delete'
	context['form'] = form
	context['order'] = order
	context['object_list'] = order.line.all()

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect(order.order_type + '-list')
		else:
			messages.add_message(request, messages.INFO, form.errors)
			print(form.errors)
	return render(request, 'paper/order/order_line_list.html', context=context)


def invoice_detail_edit(request, order_id):
	context = {}
	order = SalesOrder.objects.get(id=order_id)
	form1 = InvoiceUpdateForm(request.POST or None, instance=order)
	form2 = InvoiceAmountForm(request.POST or None, instance=order)
	context['del'] = order.order_type + '-delete'
	context['status_form'] = form1
	context['amount_form'] = form2
	context['object_list'] = order.line.all()
	if request.method == 'POST':
		# if form1.is_valid():
		order.invoice_status = request.POST.get('invoice_status', order.invoice_status)
		order.invoice_amount = request.POST.get('invoice_amount', order.invoice_amount)
		order.save()
		messages.add_message(request, messages.INFO, form1.errors, form2.errors)
	return render(request, 'paper/order/invoice_detail.html', context=context)


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
	page_number = request.GET.get('page', 1)
	page_size = request.GET.get('page_size', 10)
	queryset = OrderFilter(request.GET, queryset=queryset)
	context['filter_form'] = queryset.form
	# import pdb;pdb.set_trace()
	paginator = Paginator(queryset.qs, page_size)
	try:
		page_number = paginator.validate_number(page_number)
	except EmptyPage:
		page_number = paginator.num_pages
	filter = paginator.get_page(page_number)
	context['filter'] = filter
	context['order_type'] = 'Cancelled'
	context["breadcrumbs"] = settings.BREAD.get('cancelled_order')
	return render(request, 'paper/order/cancelled_order_list.html', context=context)


class SalesOrderDetailView(UpdateView):
	queryset = SalesOrder.objects.all().filter(is_confirmed=True).select_related('dealer').prefetch_related('line')
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
	extra_context = {
		"breadcrumbs": settings.BREAD.get('salesorder-list')
	}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['orderform'] = QuotationForm
		context['orderlineform'] = QuotationLineForm
		context['order_type'] = 'SalesOrder'
		context['filter'] = OrderFilter(self.request.GET, queryset=self.get_queryset())
		page_number = self.request.GET.get('page', 1)
		page_size = self.request.GET.get('page_size', 10)
		queryset = OrderFilter(self.request.GET, queryset=self.get_queryset())
		context['filter_form'] = queryset.form
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
	template_name = 'paper/order/salesorder_list.html'
	model = SalesOrder
	success_url = '/order/order/list'

	def get(self, request, *args, **kwargs):
		# import pdb;pdb.set_trace()
		print(self.get_object().delete())
		return redirect('salesorder-list')


class QuotationDetailView(UpdateView):
	queryset = SalesOrder.objects.all().filter(is_quotation=True).select_related('dealer').prefetch_related('line')
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
	extra_context = {
		"breadcrumbs": settings.BREAD.get('quotation-list')
	}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['orderform'] = QuotationForm
		context['orderlineform'] = QuotationLineForm
		# orderline_formset = inlineformset_factory(SalesOrder, SalesOrderLine, fields=('product', 'quantity'))
		# context['orderlineformset'] = orderline_formset
		context['order_type'] = 'Quotation'
		page_number = self.request.GET.get('page', 1)
		page_size = self.request.GET.get('page_size', 10)
		queryset = OrderFilter(self.request.GET, queryset=self.get_queryset())
		context['filter_form'] = queryset.form
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

		# orderline_formset = inlineformset_factory(SalesOrder, SalesOrderLine, fields=('product', 'quantity'))
		if form.is_valid():
			products = form.data.getlist('product')
			quantity = form.data.getlist('quantity')
			print(products, quantity)
			order = form.save()
			try:
				for product, quantity in zip(products, quantity):
					product = Product.objects.get(id=product)
					print(product)
					if int(quantity) <= 0:
						raise QuantityInvalidException("Invalid Quantity")

					line = SalesOrderLine.objects.create(product=product, quantity=quantity, order=order)
					print(f"line created {line} for order {order}")
					print(f"order {order} created")
					messages.add_message(request, messages.INFO, f"New Order {order} has been created")
			except Exception as e:
				print(str(e))
				messages.add_message(request, messages.INFO, str(e))
		else:
			messages.add_message(request, messages.SUCCESS, form.errors)
		return redirect('quotation-list')


@method_decorator(csrf_exempt, name='dispatch')
class QuotationDeleteView(DeleteView):
	queryset = SalesOrder.objects.all().select_related('dealer')
	template_name = 'paper/order/quotation_list.html'
	model = SalesOrder
	success_url = '/order/quotation/list'

	def get(self, request, *args, **kwargs):
		# import pdb;pdb.set_trace()
		print(self.get_object().delete())
		return redirect('quotation-list')


class InvoiceDetailView(UpdateView):
	queryset = SalesOrder.objects.all().filter(is_invoice=True).select_related('dealer').prefetch_related('line')
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
	extra_context = {
		"breadcrumbs": settings.BREAD.get('invoice-list')
	}
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['orderform'] = QuotationForm
		context['orderlineform'] = QuotationLineForm
		context['order_type'] = 'Invoice'
		context['filter'] = OrderFilter(self.request.GET, queryset=self.get_queryset())
		page_number = self.request.GET.get('page', 1)
		page_size = self.request.GET.get('page_size', 10)
		queryset = OrderFilter(self.request.GET, queryset=self.get_queryset())
		context['filter_form'] = queryset.form
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
	template_name = 'paper/order/invoice_list.html'
	model = SalesOrder
	success_url = '/order/invoice/list'



