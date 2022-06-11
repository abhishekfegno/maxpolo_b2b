# New file created 
from django import forms

from apps.infrastructure.models import Branch


class BranchForm(forms.ModelForm):
	class Meta:
		model = Branch
		fields = '__all__'
