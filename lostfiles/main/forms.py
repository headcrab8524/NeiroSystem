from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_class'].empty_label = "Тип не выбран"

    class Meta:
        model = ItemCard
        fields = ['name', 'slug', 'item_class', 'photo', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError('Длина превышает 255 символов')

        return name
