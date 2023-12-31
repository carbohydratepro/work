# Generated by Django 3.2 on 2023-11-17 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_merge_20231103_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='employee_id_number',
            field=models.CharField(default=None, max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='store_code',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
