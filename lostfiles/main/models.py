from django.db import models
from django.urls import reverse


class User(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/")
    #photo = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    group = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.pk


class ItemCard(models.Model):
    name = models.CharField(max_length=255)
    item_class = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    resp_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class Item(models.Model):
    name = models.CharField(max_length=255)
    time_found = models.DateTimeField()
    place_found = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/")
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
