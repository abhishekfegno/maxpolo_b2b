# New file created 
from django import forms

from apps.user.models import Complaint


class ComplaintForm(forms.ModelForm):
	class Meta:
		model = Complaint
		fields = '__all__'