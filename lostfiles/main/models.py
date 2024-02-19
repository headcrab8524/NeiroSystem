from django.db import models
from django.urls import reverse


class User(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
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
    item_class = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True)
    content = models.TextField(blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    resp_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Карточки предметов'
        verbose_name_plural = 'Карточки предметов'
        ordering = ['time_create']


class Item(models.Model):
    name = models.CharField(max_length=255)
    time_found = models.DateTimeField()
    place_found = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/", blank=True)
    item_class = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True)


class Comment(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    time_create = models.DateTimeField(auto_now_add=True)


class UserMark(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    item_card = models.ForeignKey('ItemCard', on_delete=models.SET_NULL, null=True)


class Role(models.Model):
    name = models.CharField(max_length=255)


class Class(models.Model):
    name = models.CharField(max_length=255)
    rus_name = models.CharField(max_length=255)
