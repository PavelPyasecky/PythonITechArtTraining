# Generated by Django 3.1.7 on 2021-06-01 10:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='%m/%d/%y'),
        ),
    ]
