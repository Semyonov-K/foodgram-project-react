# Generated by Django 3.2.16 on 2023-01-12 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_favorite_options_alter_ingredient_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={},
        ),
        migrations.RemoveConstraint(
            model_name='recipeingredient',
            name='unique_recipe_ingredient',
        ),
    ]
