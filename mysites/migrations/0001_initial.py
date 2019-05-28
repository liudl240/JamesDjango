# Generated by Django 2.2.1 on 2019-05-28 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='servicelist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True)),
                ('desLink', models.CharField(max_length=256)),
                ('jumpLink', models.CharField(max_length=254, unique=True)),
            ],
            options={
                'db_table': 'servicelist',
            },
        ),
    ]
