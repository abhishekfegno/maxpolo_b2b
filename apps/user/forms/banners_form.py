# New file created 
from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.user.models import Banners, Dealer, Executive


class BannersForm(forms.ModelForm):

    class Meta:
        model = Banners
        fields = ('title', 'photo')


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    # def clean(self):
    # 	if self.new_password == self.confirm_password:
    # 		return super().clean()
    # 	else:
    # 		raise ValidationError("The given passwords dont match !!")

    class Meta:
        fields = ('new_password', 'confirm_password')


class DealerForm(UserCreationForm):

    class Meta:
        model = Dealer
        fields = ('username', "password1", "password2", 'first_name', 'last_name', 'branch', 'mobile', 'email')


class ExecutiveForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dealers'].queryset = Dealer.objects.all()

    class Meta:
        model = Executive
        fields = ('username', "password1", "password2", 'first_name', 'last_name', 'branch', 'mobile', 'email', 'dealers')
