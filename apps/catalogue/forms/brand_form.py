# New file created 
from django import forms

from apps.catalogue.models import Brand


class BrandForm(forms.ModelForm):
	class Meta:
		model = Brand
		fields = '__all__'