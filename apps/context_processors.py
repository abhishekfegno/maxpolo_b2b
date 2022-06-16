from apps.user.models import SiteConfiguration


def settings(request):
    data = {}
    from django.conf import settings
    logo = SiteConfiguration.objects.first().site_logo
    data['settings'] = settings
    if logo:
        data[logo] = logo.url

    return data
