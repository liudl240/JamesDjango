from django.db import models

# Create your models here.

class tasks(models.Model):
    '''任务表'''
    GENDER_CHOICES = (
        (1, '不急'),
        (2, '正常'),
        (3, '紧急'),
        (4, '加急'),
        (5, '重要'),
        (6, '加重'),
        (7, '不急重要'),
        (8, '不急加重'),
    )
    GENDER_CHOICES1 = (
        (0, '未启动'),
        (1, '进行中'),
        (2, '完成'),
    )

    id = models.AutoField(primary_key=True)
    tasktype = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name='任务类型')
    title = models.CharField(max_length=128,null=False)
    description = models.FileField(null=True)
    tags = models.CharField(max_length=128,unique=True) 
    c_time = models.DateTimeField(null=False)
    f_time = models.DateTimeField(null=True)
    m_time = models.DateTimeField(null=True)
    username = models.ForeignKey('Users.UserInfo',to_field='username',null=True,on_delete=models.CASCADE)
    doc = models.ForeignKey('wiki.doc',to_field='id',null=True,on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=GENDER_CHOICES1, default=0, verbose_name='任务状态')


    class Meta:
        db_table = 'tasks'
        ordering = ['c_time']

class task_point(models.Model):
    """记录一个大任务分开成几个小任务去完成"""
    GENDER_CHOICES = (
        (0, '未启动'),
        (1, '进行中'),
        (2, '完成'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128,null=False)
    c_time = models.DateTimeField(null=True)
    f_time = models.DateTimeField(null=True)
    status = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name='小任务状态') 
    task = models.ForeignKey('Task.tasks',to_field='id',null=True,on_delete=models.CASCADE)
    class Meta:
        db_table = 'task_point'
        ordering = ['c_time']
