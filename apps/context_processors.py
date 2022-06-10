

def settings(request):
    from django.conf import settings
    data = {'settings': settings,
            }
    return data
