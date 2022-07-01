# New file created 
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm

from apps.user.models import Banners, Dealer, Executive, Role, User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = Dealer
        fields = ("password1", "password2", 'first_name', 'last_name',
            'branch', 'mobile', 'excalation_number', 'email', 'executive', 'company_cin', 'address_street',
            'address_city', 'address_state', )


class BannersForm(forms.ModelForm):
    class Meta:
        model = Banners
        fields = ('title', 'photo')


class ResetPasswordForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError("The given passwords dont match !!")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('new_password', 'confirm_password')


class AdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', "password1", "password2", 'first_name', 'last_name', 'branch', 'mobile', 'email')

    def save(self, commit=True):
        self.instance.user_role = Role.ADMIN
        super(AdminForm, self).save(commit=commit)


class DealerForm(UserCreationForm):

    class Meta:
        model = Dealer
        fields = (
            "password1", "password2", 'first_name', 'last_name',
            'branch', 'mobile', 'excalation_number', 'email', 'executive', 'company_cin', 'address_street',
            'address_city', 'address_state', )

    def save(self, commit=True):
        self.instance.user_role = Role.DEALER
        super(DealerForm, self).save(commit=commit)


class ExecutiveForm(UserCreationForm):

    class Meta:
        model = Executive
        fields = ("password1", "password2", 'first_name', 'last_name', 'branch', 'mobile', 'email')

    def save(self, commit=True):
        self.instance.user_role = Role.EXECUTIVE
        super(ExecutiveForm, self).save(commit=commit)


class DealerUpdateForm(UserChangeForm):

    class Meta:
        model = Dealer
        fields = (
            "password", 'first_name', 'last_name',
            'branch', 'mobile', 'email', 'executive', 'company_cin', 'address_street', 'address_city',
            'address_state', )

    def save(self, commit=True):
        self.instance.user_role = Role.DEALER
        super(DealerUpdateForm, self).save(commit=commit)


class ExecutiveUpdateForm(UserChangeForm):

    class Meta:
        model = Executive
        fields = ("password", 'first_name', 'last_name', 'branch', 'mobile', 'email')

    def save(self, commit=True):
        self.instance.user_role = Role.EXECUTIVE
        super(ExecutiveUpdateForm, self).save(commit=commit)


class AdminUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("password", 'first_name', 'last_name', 'branch', 'mobile', 'email')

    def save(self, commit=True):
        self.instance.user_role = Role.ADMIN
        super(AdminUpdateForm, self).save(commit=commit)


