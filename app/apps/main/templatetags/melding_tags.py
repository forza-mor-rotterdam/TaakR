from apps.services.onderwerpen import render_onderwerp as render_onderwerp_service
from django import template

register = template.Library()


@register.simple_tag
def render_onderwerp(onderwerp_url):
    return render_onderwerp_service(onderwerp_url)
