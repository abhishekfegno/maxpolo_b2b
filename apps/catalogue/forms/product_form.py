# New file created 
from django import forms

from apps.catalogue.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
