from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from django.views.generic.edit import FormMixin
from rest_framework.authtoken.models import Token

from apps.user.forms.banners_form import ResetPasswordForm, DealerForm, ExecutiveForm
from apps.user.models import Banners, User, Role, Dealer, Executive
from lib.token_handler import token_expire_handler, is_token_expired


class UserDetailView(UpdateView):

    queryset = User.objects.all()
    template_name = 'paper/user/user_form.html'
    model = User
    form_class = DealerForm
    success_url = '/user/list/'


class UserListView(FormMixin, ListView):
    queryset = User.objects.all()
    template_name = 'paper/user/user_list.html'
    model = User
    form_class = DealerForm

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        if self.kwargs.get('role') == 32:
            queryset = Dealer.objects.all()
        if self.kwargs.get('role') == 16:
            queryset = Executive.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('role') == 32:
            context['form'] = DealerForm
            context['role'] = 'Dealer'
        if self.kwargs.get('role') == 16:
            context['form'] = ExecutiveForm
            context['role'] = 'Executive'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        role = self.kwargs.get('role')
        # import pdb;pdb.set_trace()
        if form.is_valid():
            user = form.save(commit=False)
            user.user_role = role
            user.save()
        else:
            print(form.errors)
            # role = form.data.get('user_role')
        return redirect('user-list', role=role)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    queryset = User.objects.all()
    template_name = 'paper/user/user_delete.html'
    model = User


def password_reset(request, token):
    errors = ""
    form = ResetPasswordForm(request.POST)

    if request.method == 'POST':
        try:
            token = Token.objects.get(key=token)
            if is_token_expired(token):
                return render(request, 'registration/password_reset_confirm.html', context={'errors': errors})
            token = token_expire_handler(token)

            user = User.objects.get(id=token.user.id)
            if form.is_valid():
                user.set_password(form.data.get('confirm_password'))
                user.save()
                print(user.password)
                return render(request, 'registration/password_reset_complete.html')
        except Exception as e:
            errors = str(e)

    return render(request, 'registration/password_reset_confirm.html', context={'form': form, 'errors': errors})
