from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

import main.models
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


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={}))
    middle_name = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={}))
    photo = forms.FileField(label='Фото', widget=forms.FileInput(attrs={}))
    group = forms.CharField(label='Группа', widget=forms.TextInput(attrs={}))
    email = forms.EmailField(label='Эл. почта', widget=forms.EmailInput(attrs={}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'last_name',
                  'first_name', 'middle_name', 'photo', 'group', 'email')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password')
        widgets = {}
