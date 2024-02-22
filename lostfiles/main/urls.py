from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('card/<slug:card_slug>/', show_card, name='card')
]
