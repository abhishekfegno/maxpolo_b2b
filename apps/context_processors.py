from apps.user.models import SiteConfiguration


def settings(request):
    data = {}
    from django.conf import settings
    logo = SiteConfiguration.objects.first()
    data['settings'] = settings
    if logo:
        print(logo.site_logo_url)
        data['logo'] = logo.site_logo.url

    return data
