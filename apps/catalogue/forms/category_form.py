# New file created 
from django import forms

from apps.catalogue.models import Category


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = '__all__'
