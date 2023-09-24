# Generated by Django 3.2 on 2023-09-22 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20230918_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='確定済み'),
        ),
        migrations.AddField(
            model_name='shift',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='スタッフアカウント'),
        ),
    ]
