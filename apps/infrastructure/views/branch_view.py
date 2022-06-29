# New file created
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from apps.infrastructure.forms.branch_form import BranchForm
from apps.infrastructure.models import Branch


class BranchListView(CreateView, ListView):
    queryset = Branch.objects.all()
    template_name = 'paper/infrastructure/branch_list.html'
    model = Branch
    form_class = BranchForm
    success_url = '/infrastructure/branch/list/'


class BranchDetailView(UpdateView, ListView):
    queryset = Branch.objects.all()
    template_name = 'paper/infrastructure/branch_list.html'
    model = Branch
    form_class = BranchForm
    success_url = '/infrastructure/branch/list/'


@method_decorator(decorator=csrf_exempt, name='dispatch')
class BranchDeleteView(DeleteView):
    queryset = Branch.objects.all()
    template_name = 'templates/branch_delete.html'
    model = Branch
    success_url = '/infrastructure/branch/list/'
