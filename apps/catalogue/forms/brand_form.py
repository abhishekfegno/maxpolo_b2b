# New file created 
from django import forms

from apps.catalogue.models import Brand


class BrandForm(forms.ModelForm):
	class Meta:
		model = Brand
		fields = '__all__'

	# def clean(self):
	# 	# import pdb;pdb.set_trace()
	# 	self.validate_unique()
	# 	return self.cleaned_data
