# New file created 
from django import forms
from django.core.exceptions import ValidationError

from apps.user.models import Banners


class BannersForm(forms.ModelForm):
	class Meta:
		model = Banners
		fields = ('title', 'photo', 'is_public')


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
