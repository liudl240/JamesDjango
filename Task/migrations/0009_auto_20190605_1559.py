# Generated by Django 2.2.1 on 2019-06-05 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Task', '0008_auto_20190605_1538'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task_point',
            options={'ordering': ['c_time']},
        ),
    ]