# Generated by Django 3.1.7 on 2021-05-05 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_auto_20210505_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='author_id',
            field=models.BigIntegerField(),
        ),
    ]