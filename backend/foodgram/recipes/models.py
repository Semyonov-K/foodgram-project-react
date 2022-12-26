from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser

COUNT_SYMBOL = 15


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = ColorField(
        unique=True,
        max_length=7,
        blank = True,
        null = True,
        default = '#FFFFE0'
    )
    slug = models.SlugField(unique=True, max_length=200)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(
        Tag,
        null=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        null=True
    )
    cooking_time = models.IntegerField()
    text = models.TextField()
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        blank=True
    )

    def __str__(self):
        return str(self.text)[:COUNT_SYMBOL]


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite',
            ),
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='carts',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        ]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
    )
    amount = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_recipe_ingredient',
            ),
        )

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'
