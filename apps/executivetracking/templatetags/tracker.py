from django import template

register = template.Library()


@register.simple_tag
def get_time_diff(a, b=None):
    return
