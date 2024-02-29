from django.db import models
from django.urls import reverse


class User(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, blank=True)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    group = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.pk

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']


class ItemCard(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    item_class = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    time_found = models.DateTimeField(null=True)
    place_found = models.CharField(max_length=255, null=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    resp_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('card', kwargs={'card_slug': self.slug})

    class Meta:
        verbose_name = 'Карточки предметов'
        verbose_name_plural = 'Карточки предметов'
        ordering = ['time_create']


class Comment(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    item_card = models.ForeignKey('ItemCard', on_delete=models.SET_NULL, null=True, blank=True)


class UserMark(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    item_card = models.ForeignKey('ItemCard', on_delete=models.SET_NULL, null=True)


class Role(models.Model):
    name = models.CharField(max_length=255)


class Class(models.Model):
    name = models.CharField(max_length=255)
    rus_name = models.CharField(max_length=255)

    def __str__(self):
        return self.rus_name


class Location(models.Model):
    name = models.CharField(max_length=255)
