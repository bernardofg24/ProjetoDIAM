# Generated by Django 4.0.3 on 2022-05-15 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelcheck', '0014_remove_review_dislike_remove_review_like_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leveluser',
            name='joined',
            field=models.DateField(verbose_name='Joined'),
        ),
    ]
