# Generated by Django 3.2 on 2023-11-02 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20231102_0344'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='memo',
            field=models.TextField(null=True, default=None, blank=True),
        ),
    ]
