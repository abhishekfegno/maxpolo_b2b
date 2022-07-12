# New file created 
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm

from apps.executivetracking.models import Zone
from apps.user.models import Banners, Dealer, Executive, Role, User, SiteConfiguration


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = Dealer
        fields = ('first_name', 'last_name',
                  'branch', 'mobile', 'email', 'executive', 'company_cin', 'address_street',
                  'address_city', 'address_state', "password1", "password2", )


class BannersForm(forms.ModelForm):
    class Meta:
        model = Banners
        fields = ('title', 'photo')


class ResetPasswordForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        # import pdb;pdb.set_trace()
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
    address_street = forms.CharField(required=False)
    company_cin = forms.CharField(required=False)

    class Meta:
        model = Dealer
        fields = (
            'first_name', 'last_name', 'username',  "password1", "password2", 'zone',
            'mobile', 'email', 'executive', 'company_cin', 'address_street',
            'address_city', 'address_state', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executive'].queryset = Executive.objects.filter()
        # self.fields['company_cin'].required = False
        # self.fields['address_street'].required = False

    def save(self, commit=True):
        self.instance.user_role = Role.DEALER
        super(DealerForm, self).save(commit=commit)


class ExecutiveForm(UserCreationForm):

    class Meta:
        model = Executive
        fields = ('first_name', 'last_name', 'username', "password1", "password2", 'branch', 'mobile', 'email')

    def save(self, commit=True):
        self.instance.user_role = Role.EXECUTIVE
        super(ExecutiveForm, self).save(commit=commit)


class DealerUpdateForm(UserChangeForm):
    address_street = forms.CharField(required=False)
    company_cin = forms.CharField(required=False)

    class Meta:
        model = Dealer
        fields = (
            'first_name', 'last_name', 'username',
            'zone', 'mobile', 'email', 'executive', 'company_cin', 'address_street', 'address_city',
            'address_state', "password",
        )

    def __init__(self, *args, **kwargs):
        super(DealerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['executive'].queryset = Executive.objects.filter()

    def save(self, commit=True):
        self.instance.user_role = Role.DEALER
        super(DealerUpdateForm, self).save(commit=commit)


class ExecutiveUpdateForm(UserChangeForm):

    class Meta:
        model = Executive
        fields = ("password", 'username', 'first_name', 'last_name', 'branch', 'mobile', 'email')

    def save(self, commit=True):
        self.instance.user_role = Role.EXECUTIVE
        super(ExecutiveUpdateForm, self).save(commit=commit)


class AdminUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("password", 'username', 'first_name', 'last_name', 'branch', 'mobile', 'email')

    def save(self, commit=True):
        self.instance.user_role = Role.ADMIN
        super(AdminUpdateForm, self).save(commit=commit)



class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'


class ExcalationNumberForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = ('excalation_number',)

    def clean(self):
        if self.cleaned_data['excalation_number'].isalpha:
            raise ValueError("Invalid Input !")
        if len(self.cleaned_data['excalation_number']) > 10:
            raise ValueError("Enter a valid contact number !")

        return super().clean()