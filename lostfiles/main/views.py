from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from .utils import *


class MainHome(DataMixin, ListView):
    paginate_by = 10
    model = ItemCard
    template_name = 'main/index.html'
    context_object_name = 'cards'

    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context['itemclass'] = Class.objects.all()
        #context = dict(list(context.items())) + list(c_def.items())
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return ItemCard.objects.filter(status=True).order_by('-time_create')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddCardForm
    template_name = 'main/addpage.html'
    success_url = reverse_lazy('main')
    login_url = reverse_lazy('main') #куда перенаправлять неавторизованных
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление карточки")
        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    return HttpResponse(request, "Обратная связь")


class ShowCard(DataMixin, DetailView):
    model = ItemCard
    template_name = 'main/card.html'
    slug_url_kwarg = 'card_slug'
    context_object_name = 'card'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['card'])
        context['comment'] = Comment.objects.filter = [context['card'].pk == 'item_card']
        # context['title'] = context['card']
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


class CurrentUserProfile(DataMixin, DetailView):
    model = CustomUser
    template_name = 'main/profile.html'
    slug_url_kwarg = 'username'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['username'])
        return dict(list(context.items()) + list(c_def.items()))


class UserProfile(DataMixin, DetailView):
    model = CustomUser
    template_name = 'main/user.html'
    slug_url_kwarg = 'username'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['username'])
        return dict(list(context.items()) + list(c_def.items()))
