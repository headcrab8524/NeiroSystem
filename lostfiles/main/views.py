from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *

menu = [
    {'title': "Войти", 'url_name': 'login'}
]


class MainHome(ListView):
    model = ItemCard
    template_name = 'main/index.html'
    context_object_name = 'cards'

    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Главная страница"
        context['itemclass'] = Class.objects.all()
        return context

    def get_queryset(self):
        return ItemCard.objects.filter(status=True)


class AddPage(CreateView):
    form_class = AddCardForm
    template_name = 'main/addpage.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Добавление карточки"
        return context


def contact(request):
    return HttpResponse(request, "Обратная связь")


def login(request):
    return HttpResponse(request, "Авторизация")


class ShowCard(DetailView):
    model = ItemCard
    template_name = 'main/card.html'
    slug_url_kwarg = 'card_slug'
    context_object_name = 'card'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['comment'] = Comment.objects.filter = [context['card'].pk == 'item_card']
        # context['title'] = context['card']
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Данной страницы не существует</h1>')
