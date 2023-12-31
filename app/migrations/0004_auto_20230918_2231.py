# Generated by Django 3.2 on 2023-09-18 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_alter_shift_applicant_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shift',
            name='applicant_name',
            field=models.CharField(max_length=200, verbose_name='申請者の名前'),
        ),
    ]
