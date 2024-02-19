from django import template
from main.models import *

register = template.Library()


@register.simple_tag()
def get_class():
    return Class.objects.all().values("rus_name")
