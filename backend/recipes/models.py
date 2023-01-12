from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import CustomUser

COUNT_SYMBOL = 15


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тэга'
    )
    color = ColorField(
        unique=True,
        max_length=7,
        blank = True,
        null = True,
        default = '#FFFFE0'
    )
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        null=True,
        verbose_name='Тэг'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        null=True,
        verbose_name='Ингредиенты'
    )
    cooking_time = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
        ],
        verbose_name='Время приготовления'
    )

    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True,
        verbose_name='Фото рецепта'
    )

    def __str__(self):
        return str(self.text)[:COUNT_SYMBOL]
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite',
            ),
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name = 'Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name = 'Ингредиент'
    )
    amount = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
        ],
        verbose_name = 'Количество ингредиентов'
    )

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'
