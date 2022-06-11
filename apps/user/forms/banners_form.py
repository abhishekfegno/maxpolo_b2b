# New file created 
from django import forms

from apps.user.models import Banners


class BannersForm(forms.ModelForm):
	class Meta:
		model = Banners
		fields = ('title', 'photo')
