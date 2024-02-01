from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def index(request): #HttpRequest
    if request.GET:
        print(request.GET)

    return HttpResponse("Главная страницв")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Лол кек деняк нет</h1>')
