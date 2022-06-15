    # New file created
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from rest_framework.authtoken.models import Token

from apps.user.forms.banners_form import BannersForm, ResetPasswordForm, DealerForm, ExecutiveForm
from apps.user.models import Banners, User, Role
from lib.token_handler import token_expire_handler, is_token_expired


class UserDetailView(UpdateView):

    queryset = User.objects.all()
    template_name = 'paper/user/user_form.html'
    model = User
    form_class = DealerForm
    success_url = '/user/list/'


class UserListView(CreateView, ListView):
    queryset = User.objects.all()
    template_name = 'paper/user/user_list.html'
    model = Banners
    form_class = DealerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('role') == 32:
            context['form'] = DealerForm
            context['role'] = 'Dealer'
            context['object_list'] = User.objects.filter(user_role=Role.DEALER)
        if self.kwargs.get('role') == 16:
            context['form'] = ExecutiveForm
            context['role'] = 'Executive'
            context['object_list'] = User.objects.filter(user_role=Role.EXECUTIVE)
        return context


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    queryset = User.objects.all()
    template_name = 'paper/user/user_delete.html'
    model = Banners


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
