# Generated by Django 4.0.4 on 2022-05-13 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelcheck', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leveluser',
            old_name='leveluser',
            new_name='user',
        ),
    ]
