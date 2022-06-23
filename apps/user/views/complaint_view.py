# New file created
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from django_filters.rest_framework import DjangoFilterBackend

from apps.user.forms.complaint_form import ComplaintForm
from apps.user.models import Complaint
from lib.filters import ComplaintFilter
from lib.importexport import ComplaintReport


def get_excel_report_complaint(request):
    queryset = Complaint.objects.select_related('created_by')
    name = 'complaints'
    dataset = ComplaintReport().export(queryset)
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{name}.xls"'
    return response


class ComplaintDetailView(UpdateView):
	queryset = Complaint.objects.all()
	template_name = 'paper/user/complaint_form.html'
	model = Complaint
	form_class = ComplaintForm
	success_url = '/complaint/list'


class ComplaintListView(CreateView, ListView):
	queryset = Complaint.objects.all()
	template_name = 'paper/user/complaint_list.html'
	model = Complaint
	form_class = ComplaintForm
	success_url = '/complaint/list'
	filtering_backends = (DjangoFilterBackend,)
	filtering_class = ComplaintFilter
	filterset_fields = ('status',)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = ComplaintForm
		page_number = self.request.GET.get('page', 1)
		page_size = self.request.GET.get('page_size', 10)
		queryset = ComplaintFilter(self.request.GET, queryset=self.get_queryset())
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


@method_decorator(csrf_exempt, name='dispatch')
class ComplaintDeleteView(DeleteView):
	queryset = Complaint.objects.all()
	template_name = 'paper/user/complaint_delete.html'
	model = Complaint
	success_url = '/complaint/list'


