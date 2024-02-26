from django import forms
from .models import *


class AddCardForm(forms.Form):
    name = forms.CharField(max_length=255, label="Название")
    slug = forms.SlugField(max_length=255, label="URL")
    item_class = forms.ModelChoiceField(queryset=Class.objects.all().values("rus_name"),
                                        label="Тип предмета", empty_label="Тип не выбран")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Описание", required=False)
