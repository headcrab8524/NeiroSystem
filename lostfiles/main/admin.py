from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'middle_name', 'last_name')
    list_display_links = ()
    search_fields = ('first_name', 'middle_name', 'last_name',
                     'role', 'group', 'email')
    list_editable = ()

    fields = ()
    readonly_fields = ()

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Аватар"


class ItemCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_html_photo', 'item_class', 'time_create', 'resp_user', 'status')
    list_display_links = ()
    search_fields = ('name', 'item_class', 'resp_user', 'status')
    list_editable = ()
    list_filter = ('item_class', 'resp_user', 'status')

    fields = ()
    readonly_fields = ()

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Фото предмета"


class CommentAdmin(admin.ModelAdmin):
    list_display = ('item_card', 'user', 'time_create', 'text')
    list_display_links = ()
    search_fields = ('item_card', 'user', 'time_create')
    list_editable = ()
    list_filter = ('item_card', 'user', 'time_create')


class UserMarkAdmin(admin.ModelAdmin):
    list_display = ('item_card', 'user')
    list_display_links = ()
    search_fields = ('item_card', 'user')
    list_editable = ()
    list_filter = ('item_card', 'user')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ()
    search_fields = ('id', 'name')
    list_editable = ()


class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rus_name')
    list_display_links = ()
    search_fields = ('id', 'name', 'rus_name')
    list_editable = ()


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ()
    search_fields = ('id', 'name')
    list_editable = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.register(ItemCard, ItemCardAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserMark, UserMarkAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Location, LocationAdmin)


admin.site.site_title = 'Админ-панель сайта'
admin.site.site_header = 'Админ-панель сайта'
