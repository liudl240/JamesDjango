# Generated by Django 2.2.1 on 2019-05-28 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_userinfo_l_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='l_time',
            field=models.DateTimeField(),
        ),
    ]
