# New file created 
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView

from apps.infrastructure.forms.branch_form import BranchForm
from apps.infrastructure.models import Branch


class BranchDetailView(UpdateView):
	queryset = Branch.objects.all()
	template_name = 'paper/infrastructure/branch_form.html'
	model = Branch
	form_class = BranchForm
	success_url = '/infrastructure/branch/list/'


class BranchListView(CreateView, ListView):
	queryset = Branch.objects.all()
	template_name = 'paper/infrastructure/branch_list.html'
	model = Branch
	form_class = BranchForm
	success_url = '/infrastructure/branch/list/'


class BranchDeleteView(DeleteView):
	queryset = Branch.objects.all()
	template_name = 'templates/branch_delete.html'
	model = Branch
	success_url = '/infrastructure/branch/list/'


