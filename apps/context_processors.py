from django.urls import resolve

from apps.user.models import SiteConfiguration


def settings(request):
    data = {}
    logo = SiteConfiguration.objects.first()

    data['settings'] = settings
    view_name = resolve(request.path_info).url_name
    data['current_url'] = view_name.split('-')[0].capitalize()

    if logo:
        data['logo'] = logo.site_logo.url
    return data
