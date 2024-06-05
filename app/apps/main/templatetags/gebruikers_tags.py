from django import template
from django.contrib.auth import get_user_model
from utils.diversen import gebruikersnaam as gebruikersnaam_basis

register = template.Library()


@register.filter
def gebruikersnaam(value):
    return gebruikersnaam_basis(value)
