# Generated by Django 4.2.4 on 2023-11-02 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_rename_recipe_favorite_favorite_recipe'),
        ('recipes', '0015_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
