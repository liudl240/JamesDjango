# Generated by Django 2.2.1 on 2019-06-11 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0009_auto_20190611_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='Avatar_name',
            field=models.CharField(default='cat.jpg', max_length=200),
        ),
    ]
