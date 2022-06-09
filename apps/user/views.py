from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, TemplateView


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
            pass
