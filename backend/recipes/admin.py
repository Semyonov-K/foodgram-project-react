from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'color',
        'slug',

    )
    list_editable = (
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_editable = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = ('id', 'recipe', 'ingredient')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'author',
        'get_favorites',
    )
    list_editable = (
        'name',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    search_fields = (
        'name',
    )
    inlines = (RecipeIngredientsInline,)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Автоподстановка текущего пользователя в авторы рецепта при
        создании через Админку."""
        field = super(RecipeAdmin, self).formfield_for_dbfield(
            db_field, **kwargs
        )
        if db_field.name == "author":
            field.initial = kwargs["request"].user.id
        return field

    def get_favorites(self, obj):
        return obj.favorite.count()

    get_favorites.short_description = (
        'Число добавлений в избранное'
    )
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'user',
        'recipe',
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'user',
        'recipe',
    )
