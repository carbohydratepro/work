# Generated by Django 3.2 on 2023-08-29 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_name', models.CharField(max_length=200, verbose_name='申請者の名前')),
                ('substitute_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='代役の名前')),
                ('start_time', models.DateTimeField(verbose_name='開始時間')),
                ('end_time', models.DateTimeField(verbose_name='終了時間')),
                ('is_substitute_found', models.BooleanField(default=False, verbose_name='代役が見つかっている')),
            ],
        ),
    ]
