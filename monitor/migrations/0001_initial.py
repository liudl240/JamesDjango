# Generated by Django 2.2.1 on 2019-08-01 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.CharField(max_length=200)),
                ('product', models.CharField(max_length=200)),
                ('buy_time', models.DateTimeField()),
                ('exprie_time', models.DateTimeField(null=True)),
                ('price', models.CharField(max_length=200)),
                ('application', models.CharField(max_length=200)),
                ('num', models.IntegerField()),
                ('urladdress', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'company',
                'ordering': ['exprie_time'],
            },
        ),
    ]
