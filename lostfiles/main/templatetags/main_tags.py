from django import template
from main.models import *

register = template.Library()


@register.simple_tag()
def get_class(filter=None):
    if not filter:
        return Class.objects.all().values("rus_name")
    else:
        return Class.objects.all().values("rus_name").filter(pk=filter)


@register.inclusion_tag('main/list_categories.html')
def show_class(sort=None, class_selected=0):
    if not sort:
        classes = Class.objects.all().values("rus_name")
    else:
        classes = Class.objects.all().values("rus_name").order_by(sort)

    return {"classes": classes, "class_selected": class_selected}
