# New file created
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.user.forms.complaint_form import ComplaintForm
from apps.user.models import Complaint


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


@method_decorator(csrf_exempt, name='dispatch')
class ComplaintDeleteView(DeleteView):
	queryset = Complaint.objects.all()
	template_name = 'paper/user/complaint_delete.html'
	model = Complaint
	success_url = '/complaint/list'


