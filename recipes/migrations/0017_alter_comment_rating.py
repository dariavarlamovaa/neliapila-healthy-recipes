# Generated by Django 5.0b1 on 2023-11-02 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_rename_comments_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(),
        ),
    ]
