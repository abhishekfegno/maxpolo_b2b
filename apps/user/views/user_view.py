from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, DeleteView, ListView, TemplateView
from django.views.generic.edit import FormMixin
from rest_framework.authtoken.models import Token

from apps.user.forms.banners_form import ResetPasswordForm, DealerForm, ExecutiveForm
from apps.user.models import Banners, User, Dealer, Executive
from lib.token_handler import token_expire_handler, is_token_expired


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['advertisements'] = Banners.objects.all()
        return self.render_to_response(context)


class UserDetailView(UpdateView):
    queryset = User.objects.all()
    form_class = UserCreationForm
    template_name = 'paper/user/user_list.html'
    model = User
    success_url = '/user/list/'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
        else:
            print(form.errors)
        role = form.instance.user_role
        return redirect('user-list', role=role)


class UserListView(FormMixin, ListView):
    queryset = User.objects.all()
    form_class = UserCreationForm
    template_name = 'paper/user/user_list.html'
    home_label = _("User list")
    model = User

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        if self.kwargs.get('role') == 'dealer':
            queryset = Dealer.objects.all()
        if self.kwargs.get('role') == 'executive':
            queryset = Executive.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('role') == 'dealer':
            context['form'] = DealerForm
            context['role'] = 'Dealer'
        if self.kwargs.get('role') == 'executive':
            context['form'] = ExecutiveForm
            context['role'] = 'Executive'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        role = self.kwargs.get('role')
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
    template_name = 'paper/user/user_list.html'
    model = User
    success_url = '/user/list/'


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
