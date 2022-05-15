# Generated by Django 4.0.3 on 2022-05-15 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelcheck', '0019_remove_usercharacters_user_character_favourites_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercharacters',
            name='type',
            field=models.CharField(choices=[('F', 'Favourite'), ('U', 'Unfavourite')], default='1', max_length=1),
            preserve_default=False,
        ),
    ]