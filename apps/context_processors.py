from django.urls import resolve
from apps.user.models import SiteConfiguration


def settings(request):
    data = {}
    from django.conf import settings as django_settings
    logo = SiteConfiguration.objects.first()
    data['settings'] = django_settings
    data['current_url'] = resolve(request.path_info).url_name
    if logo:
        data['logo'] = logo.site_logo.url
    return data
