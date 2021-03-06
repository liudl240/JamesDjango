# Generated by Django 2.2.1 on 2019-06-09 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_auto_20190606_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='Avatar',
            field=models.ImageField(default='/Avatar/cat.jpg', upload_to='Avatar'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='Avatar_name',
            field=models.CharField(default='cat.jpg', max_length=128),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='cellphone',
            field=models.CharField(default='', max_length=11, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(default='', max_length=128, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='remark',
            field=models.CharField(default='', max_length=244, verbose_name='简介备注'),
        ),
    ]
