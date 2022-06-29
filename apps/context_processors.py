from django.urls import resolve

from apps.user.models import SiteConfiguration


def settings(request):
    data = {}
    from django.conf import settings as django_settings
    logo = SiteConfiguration.objects.first()

    data['settings'] = django_settings
    view_name = resolve(request.path_info).url_name
    if view_name:
        data['current_url'] = view_name.split('-')[0].capitalize()
    if logo:
        data['logo'] = logo.site_logo.url
    print(data['settings'].SITE_NAME)
    return data
