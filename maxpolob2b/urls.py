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
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

import lib.root
from .settings import DEBUG


def index(request):
    return render(request, 'contact-us.html', )


urlpatterns = [
    path('pages/', include('django.contrib.flatpages.urls')),
    path('admin/', admin.site.urls),
    path('', include([
        path('', include('apps.user.urls')),
        path('auth/', include('django.contrib.auth.urls')),
        path('catalogue/', include('apps.catalogue.urls')),
        path('order/', include('apps.order.urls')),
        path('infrastructure/', include('apps.infrastructure.urls')),
        path('payment/', include('apps.payment.urls')),
        path('punch-report/', include('apps.executivetracking.urls')),
    ])),

    path('api/v1/', include([
        path('', lib.root.api_root),
        path('catalogue/', include('apps.catalogue.api.urls')),
        path('user/', include('apps.user.api.urls')),
        path('order/', include('apps.order.api.urls')),
        path('payment/', include('apps.payment.api.urls')),
        path('notification/', include('apps.notification.api.urls')),
        path('tracking/', include('apps.executivetracking.api_urls')),
    ])),
    path('__debug__/', include(debug_toolbar.urls)),
    # path('contact-us.html', index, name="contact-us")
]
if DEBUG:
    urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
                    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

