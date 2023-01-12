# Generated by Django 3.2.16 on 2023-01-12 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20230112_2159'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'Ингредиент Рецепта', 'verbose_name_plural': 'Ингредиенты Рецепта'},
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_recipe_ingredient'),
        ),
    ]