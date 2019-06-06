# Generated by Django 2.2.1 on 2019-05-31 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='content',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='doc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wiki.doc'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Users.UserInfo', to_field='username'),
        ),
    ]