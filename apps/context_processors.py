from apps.user.models import SiteConfiguration
from django.urls import resolve


def settings(request):
    data = {}
    from django.conf import settings
    logo = SiteConfiguration.objects.first()
    data['settings'] = settings
    print(dir(request))
    print(request.body)


    data['current_url'] = resolve(request.path_info).url_name
    if logo:
        data['logo'] = logo.site_logo.url
    return data
