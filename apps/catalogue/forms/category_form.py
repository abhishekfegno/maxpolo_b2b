# New file created 
from django import forms
from django.core.validators import FileExtensionValidator
from treebeard.forms import MoveNodeForm

from apps.catalogue.models import Category, PDF


class CategoryForm(MoveNodeForm):
    class Meta:
        model = Category
        exclude = ('sib_order', 'parent', 'path', 'depth', 'numchild')


class PDFForm(forms.ModelForm):
    file = forms.FileField(validators=[FileExtensionValidator(['pdf'])])

    class Meta:
        model = PDF
        fields = ('title', 'file', 'image', 'category')
