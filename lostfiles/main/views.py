from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def index(request):  # HttpRequest
    context = {

    }
    return render(request, 'main/index.html', context=context)


def addpage(request): # HttpRequest
    return HttpResponse(request, "Добавление карточки")


def contact(request):
    return HttpResponse(request, "Обратная связь")


def login(request):
    return HttpResponse(request, "Авторизация")


def show_post(request, post_id):
    return HttpResponse(f"Отображение карточки с id = {post_id}")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Данной страницы не существует</h1>')
