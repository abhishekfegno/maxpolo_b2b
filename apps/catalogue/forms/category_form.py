# New file created 
from django import forms

from apps.catalogue.models import Category, PDF


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = '__all__'


class PDFForm(forms.ModelForm):
	class Meta:
		model = PDF
		fields = ('title', 'file', 'category', 'is_public')

