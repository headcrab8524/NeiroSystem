from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    middle_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, blank=True, verbose_name="Фото")
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Роль", default=2)
    group = models.CharField(max_length=255, null=True, blank=True, verbose_name="Группа")
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name="Эл. почта")

    USERNAME_FIELD = 'username'

    def get_absolute_url(self):
        return reverse('user', kwargs={'user_id': self.pk})

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']


class ItemCard(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    item_class = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, verbose_name="Тип предмета")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Фото")
    time_found = models.DateTimeField(null=True, verbose_name="Время нахождения")
    place_found = models.CharField(max_length=255, null=True, verbose_name="Место нахождения")
    content = models.TextField(blank=True, verbose_name="Описание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    resp_user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, verbose_name="Ответственный")
    status = models.BooleanField(default=True, verbose_name="Статус")

    def get_absolute_url(self):
        return reverse('card', kwargs={'card_slug': self.slug})

    class Meta:
        verbose_name = 'Карточки предметов'
        verbose_name_plural = 'Карточки предметов'
        ordering = ['time_create']


class Comment(models.Model):
    text = models.CharField(max_length=255, verbose_name="Текст")
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    item_card = models.ForeignKey('ItemCard', on_delete=models.SET_NULL, null=True,
                                  blank=True, verbose_name="Карточка предмета")

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ['time_create']


class UserMark(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    item_card = models.ForeignKey('ItemCard', on_delete=models.SET_NULL, null=True, verbose_name="Карточка предмета")

    class Meta:
        verbose_name = 'Отметки пользователей'
        verbose_name_plural = 'Отметки пользователей'
        ordering = ['item_card']


class Role(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('role', kwargs={'role_id': self.pk})

    class Meta:
        verbose_name = 'Роли'
        verbose_name_plural = 'Роли'
        ordering = ['id']


class Class(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    rus_name = models.CharField(max_length=255, verbose_name="Название на русском")

    def __str__(self):
        return self.rus_name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Типы предметов'
        verbose_name_plural = 'Типы предметов'
        ordering = ['id']


class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = 'Места нахождения'
        verbose_name_plural = 'Места нахождения'
        ordering = ['id']
