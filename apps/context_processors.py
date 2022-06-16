from apps.user.models import SiteConfiguration


def settings(request):
    from django.conf import settings

    data = {'settings': settings,
            'logo': SiteConfiguration.objects.first().site_logo.url
            }
    return data
