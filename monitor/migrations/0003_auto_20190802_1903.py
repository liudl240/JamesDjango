# Generated by Django 2.2.1 on 2019-08-02 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20190801_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='buy_time',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='exprie_time',
            field=models.CharField(max_length=100, null=True),
        ),
    ]