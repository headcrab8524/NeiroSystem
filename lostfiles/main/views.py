from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .models import *

menu = [
    {'title': "Войти", 'url_name': 'login'}
]


def index(request):  # HttpRequest
    cards = ItemCard.objects.all()
    return render(request, 'main/index.html', { 'cards' :cards })


def addpage(request): # HttpRequest
    return HttpResponse(request, "Добавление карточки")


def contact(request):
    return HttpResponse(request, "Обратная связь")


def login(request):
    return HttpResponse(request, "Авторизация")


def show_card(request, card_slug):
    card = get_object_or_404(ItemCard, slug=card_slug)

    context = {
        'card': card,
        'menu': menu,
        'title': ItemCard.name,
        'class_selected': card.item_class,
    }

    return render(request, 'main/card.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Данной страницы не существует</h1>')
