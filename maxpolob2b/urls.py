"""maxpolob2b URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import lib.root
from .settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.user.urls')),
    path('catalogue/', include('apps.catalogue.urls')),
    path('order/', include('apps.order.urls')),
    path('infrastructure/', include('apps.infrastructure.urls')),
    path('api/v1/', include([
        path('', lib.root.api_root),
        path('catalogue/', include('apps.catalogue.api.urls')),
        path('user/', include('apps.user.api.urls')),
        path('order/', include('apps.order.api.urls')),
    ])),
    path('__debug__/', include('debug_toolbar.urls')),

]
if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
