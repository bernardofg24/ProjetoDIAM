# Generated by Django 4.0.4 on 2022-05-14 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelcheck', '0002_rename_leveluser_leveluser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='img_src',
        ),
        migrations.AddField(
            model_name='game',
            name='img',
            field=models.ImageField(default=5, upload_to='images/'),
            preserve_default=False,
        ),
    ]