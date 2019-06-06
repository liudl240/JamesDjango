# Generated by Django 2.2.1 on 2019-05-31 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Task', '0002_auto_20190531_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='task_point',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('c_time', models.DateTimeField(null=True)),
                ('t_time', models.DateTimeField(null=True)),
                ('status', models.SmallIntegerField(choices=[(1, '未开始'), (2, '进行中'), (3, '结束')], default=1, verbose_name='未开始')),
            ],
            options={
                'db_table': 'task_point',
                'ordering': ['status'],
            },
        ),
        migrations.RemoveField(
            model_name='tasks',
            name='content',
        ),
        migrations.RemoveField(
            model_name='tasks',
            name='status',
        ),
        migrations.AddField(
            model_name='tasks',
            name='description',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='tasks',
            name='tasktype',
            field=models.SmallIntegerField(choices=[(1, '不急'), (2, '正常'), (3, '紧急'), (4, '加急'), (5, '重要'), (6, '加重'), (7, '不急重要'), (8, '不急加重')], default=1, verbose_name='任务状态'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]