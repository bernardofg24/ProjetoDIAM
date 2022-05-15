# Generated by Django 4.0.3 on 2022-05-15 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('levelcheck', '0015_alter_leveluser_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewfeedback',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='levelcheck.review'),
        ),
        migrations.AlterField(
            model_name='reviewfeedback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='feedback', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='reviewfeedback',
            constraint=models.UniqueConstraint(fields=('user', 'review'), name='user_review_feedback'),
        ),
    ]
