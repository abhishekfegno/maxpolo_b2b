# New file created 
from django import forms
from treebeard.forms import MoveNodeForm

from apps.catalogue.models import Category, PDF


class CategoryForm(MoveNodeForm):

	class Meta:
		model = Category
		exclude = ('sib_order', 'parent', 'path', 'depth', 'numchild')


class PDFForm(forms.ModelForm):
	class Meta:
		model = PDF
		fields = ('title', 'file', 'category', 'is_public')

