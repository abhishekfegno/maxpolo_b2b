# New file created 
from django.urls import path

from apps.catalogue.views.brand_view import *
from apps.catalogue.views.category_view import *
from apps.catalogue.views.product_view import *

urlpatterns = [
    path('category/list/', CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/update/', CategoryListView.as_view(), name='category-update'),
    # path('category/<int:pk>/update/', CategoryDetailView.as_view(), name='category-update'),
    path('catagory/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    path('pdf/list/', PDFListView.as_view(), name='pdf-list'),
    path('pdf/<int:pk>/', PDFListView.as_view(), name='pdf-modify'),

    path('pdf/<int:pk>/update/', PDFDetailView.as_view(), name='pdf-update'),
    path('pdf/<int:pk>/delete/', PDFDeleteView.as_view(), name='pdf-delete'),

    path('brand/list/', BrandListView.as_view(), name='brand-list'),
    path('brand/<int:pk>/update/', BrandDetailView.as_view(), name='brand-update'),
    path('brand/<int:pk>/delete/', BrandDeleteView.as_view(), name='brand-delete'),

    path('product/list/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/update/', ProductDetailView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

]
