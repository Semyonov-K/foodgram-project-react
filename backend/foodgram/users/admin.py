from django.contrib import admin

from .models import CustomUser, Follow


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
    )
    list_editable = (
        'first_name',
        'last_name',
        'role',
    )
    list_filter = (
        'username',
        'email',
    )
    search_fields = (
        'user',
        'author',
    )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'user',
        'author',
    )
