from django import template
from utils.diversen import gebruikersnaam as gebruikersnaam_basis

register = template.Library()


@register.filter
def gebruikersnaam(value):
    return gebruikersnaam_basis(value)
