from django.urls import path

from .views import *

urlpatterns = [
    path('', MainHome.as_view(), name='main'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('card/<slug:card_slug>/', ShowCard.as_view(), name='card')
]
