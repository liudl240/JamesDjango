# Generated by Django 2.2.1 on 2019-05-31 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_auto_20190531_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='img',
            field=models.ImageField(upload_to='img'),
        ),
    ]
