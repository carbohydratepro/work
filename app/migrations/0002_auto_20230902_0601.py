# Generated by Django 3.2 on 2023-09-01 21:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='日付'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='end_time',
            field=models.TimeField(verbose_name='終了時間'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='start_time',
            field=models.TimeField(verbose_name='開始時間'),
        ),
    ]
