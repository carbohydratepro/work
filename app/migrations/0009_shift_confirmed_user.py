# Generated by Django 3.2 on 2023-11-18 03:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_shift_memo'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='confirmed_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='確定したユーザー', to=settings.AUTH_USER_MODEL),
        ),
    ]
