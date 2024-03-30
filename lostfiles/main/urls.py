from django.urls import path

from .views import *

urlpatterns = [
    path('', MainHome.as_view(), name='main'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', CurrentUserProfile.as_view(), name='profile'),
    path('user/<int:user_id>/', UserProfile.as_view(), name='user'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('card/<slug:card_slug>/', ShowCard.as_view(), name='card'),
    path('category/<int:cat_id>/', ItemCategory.as_view(), name='category'),
    path('redact/<int:user_id>/', ChangeUserInfo.as_view(), name='redact'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),
    path('comment/<int:card_id>', comment, name='comment'),
    path('mark_card/<int:card_id>', mark_card, name='mark_card'),
    path('unmark_card/<int:card_id>', unmark_card, name='unmark_card'),
    path('marked', ShowMarked.as_view(), name='show_marked'),
]
