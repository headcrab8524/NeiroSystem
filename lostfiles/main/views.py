from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def index(request):  # HttpRequest
    return render(request, 'main/index.html')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Данной страницы не существует</h1>')
