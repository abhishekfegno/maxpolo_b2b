from django import template

register = template.Library()


def is_same_root(url, request):
    url = str(url)
    if url:
        if len(url) == 1:
            # special case of path = '/'; this is the starting of every url hence conflict with everything.
            return request.path_info == url
        else:
            return request.path_info.startswith(url)


@register.filter
def is_active(request, url):
    return (is_same_root(url, request) and 'active') or ''


@register.filter
def slugify(term):
    return term.lower().replace(' ', '-').strip()


@register.filter
def link_class(url, request):
    return '' if is_same_root(url, request) else 'collapsed'


@register.filter
def show_class(url, request):
    return 'active' if is_same_root(url, request) else ''


@register.filter
def collapse_class(url_list, request):
    if url_list is None:
        return ''
    for menu in url_list:
        if is_same_root(menu.get('url', []), request):
            return 'show'
    return ''


@register.filter
def menu_aria_expand(url_list, request):
    if url_list is None:
        return 'false'
    for menu in url_list:
        if is_same_root(menu.get('url', ''), request):
            return 'true'
    return 'false'


@register.filter
def show_in_submenu(url_list, request):
    if url_list is None:
        return ''
    for menu in url_list:
        if is_same_root(menu.get('url', ''), request):
            return 'show'
    return ''


@register.filter
def getattr(instance, field):
    return (hasattr(instance, field) and getattr(instance, field)) or '-'


@register.simple_tag
def params(field_name, value, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url.rstrip('&')
