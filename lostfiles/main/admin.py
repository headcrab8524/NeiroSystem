from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('role', 'username', 'password')
    list_display_links = ()
    search_fields = ('first_name', 'middle_name', 'last_name', 'login',
                     'role', 'group', 'email')
    list_editable = ()


class ItemCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_class', 'time_create', 'resp_user', 'status')
    list_display_links = ()
    search_fields = ('name', 'item_class', 'resp_user', 'status')
    list_editable = ()
    list_filter = ('item_class', 'resp_user', 'status')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(ItemCard, ItemCardAdmin)
