from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from .utils import *


class MainHome(DataMixin, ListView):
    paginate_by = 10
    model = ItemCard
    template_name = 'main/index.html'
    context_object_name = 'cards'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context['itemclass'] = Class.objects.all()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return ItemCard.objects.filter(status=True).order_by('-time_create')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddCardForm
    template_name = 'main/addpage.html'
    success_url = reverse_lazy('main')
    login_url = reverse_lazy('main')  # куда перенаправлять неавторизованных
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление карточки")
        return dict(list(context.items()) + list(c_def.items()))


class ShowCard(DataMixin, DetailView):
    model = ItemCard
    template_name = 'main/card.html'
    slug_url_kwarg = 'card_slug'
    context_object_name = 'card'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['card'].name)
        context['comment'] = Comment.objects.filter(item_card__id=context['card'].pk)
        if self.request.user.is_authenticated:
            context['user_mark'] = UserMark.objects.filter(item_card__id=context['card'].pk, user=self.request.user)
        return dict(list(context.items()) + list(c_def.items()))


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Данной страницы не существует</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('login')


class CurrentUserProfile(LoginRequiredMixin, DataMixin, ListView):
    model = CustomUser
    template_name = 'main/profile.html'
    context_object_name = 'current_user'
    pk_url_kwarg = 'user_id'
    login_url = 'main'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Профиль")
        return dict(list(context.items()) + list(c_def.items()))


class UserProfile(DataMixin, DetailView):
    model = CustomUser
    template_name = 'main/user.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = Role.objects.all()
        c_def = self.get_user_context(title="Профиль")
        return dict(list(context.items()) + list(c_def.items()))


class ItemCategory(DataMixin, ListView):
    paginate_by = 10
    model = ItemCard
    template_name = 'main/index.html'
    context_object_name = 'cards'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Фильтр по категории')
        context['itemclass'] = Class.objects.all()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return ItemCard.objects.filter(item_class=self.kwargs['cat_id'], status=True).order_by('-time_create')


class ChangeUserInfo(DataMixin, UpdateView):
    form_class = ChangeUserInfo
    model = CustomUser
    template_name = 'main/redact.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'user_id'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Редактирование профиля')
        return dict(list(context.items()) + list(c_def.items()))


def update_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    role = request.POST.get('role_select', None)
    user.role = Role.objects.get(pk=role)
    user.save()
    return redirect('user', user_id=user_id)


def comment(request, card_id):
    card = ItemCard.objects.get(pk=card_id)
    if request.method == "POST":
        text = request.POST["text"]
        new_comment = Comment(text=text, user=request.user, item_card=card)
        new_comment.save()
    return redirect('card', card_slug=card.slug)


def mark_card(request, card_id):
    card = ItemCard.objects.get(pk=card_id)

    new_mark = UserMark(item_card=card, user=request.user)
    new_mark.save()

    return redirect('card', card_slug=card.slug)


def unmark_card(request, card_id):
    card = ItemCard.objects.get(pk=card_id)
    mark = UserMark.objects.get(item_card=card, user=request.user)

    mark.delete()

    return redirect('card', card_slug=card.slug)


class ShowMarked(DataMixin, ListView):
    paginate_by = 10
    model = ItemCard
    template_name = 'main/index.html'
    context_object_name = 'cards'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Отмеченные предметы')
        context['itemclass'] = Class.objects.all()
        context['marked'] = UserMark.objects.filter(user=self.request.user)
        context['marked_cards'] = UserMark.objects.values("item_card__pk")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        marked_cards = UserMark.objects.filter(user=self.request.user).values('item_card__pk')
        return ItemCard.objects.filter(pk__in=marked_cards, status=True).order_by('-time_create')
