from apps.user.models import SiteConfiguration


def settings(request):
    data = {}
    from django.conf import settings
    logo = SiteConfiguration.objects.first()
    data['settings'] = settings
    if logo:
        data[logo] = logo.sites_logo.url

    return data
