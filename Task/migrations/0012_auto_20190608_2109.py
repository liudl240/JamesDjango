# Generated by Django 2.2.1 on 2019-06-08 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Task', '0011_auto_20190608_2037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasks',
            old_name='m_time',
            new_name='f_time',
        ),
    ]