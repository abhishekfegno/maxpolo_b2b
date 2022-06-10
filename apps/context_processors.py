

def settings(request):
    from django.conf import settings
    print(settings.STATIC_URL)
    data = {'settings': settings,
            }
    return data
