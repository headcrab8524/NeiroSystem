from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'middle_name', 'last_name')
    list_display_links = ()
    search_fields = ('first_name', 'middle_name', 'last_name',
                     'role', 'group', 'email')
    list_editable = ()


class ItemCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_class', 'time_create', 'resp_user', 'status')
    list_display_links = ()
    search_fields = ('name', 'item_class', 'resp_user', 'status')
    list_editable = ()
    list_filter = ('item_class', 'resp_user', 'status')


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
