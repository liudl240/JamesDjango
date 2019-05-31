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

    id = models.AutoField(primary_key=True)
    tasktype = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name='任务状态')
    title = models.CharField(max_length=128,null=False)
    description = models.FileField(null=True)
    tags = models.CharField(max_length=128,unique=True) 
    c_time = models.DateTimeField(null=False)
    f_time = models.DateTimeField(null=True)
    m_time = models.DateTimeField(null=True)
    username = models.ForeignKey('Users.UserInfo',to_field='username',null=True,on_delete=models.CASCADE)
    doc = models.ForeignKey('wiki.doc',to_field='id',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'tasks'
        ordering = ['c_time']

class task_point(models.Model):
    """记录一个大任务分开成几个小任务去完成"""
    GENDER_CHOICES = (
        (1, '未开始'),
        (2, '进行中'),
        (3, '结束'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128,null=False)
    c_time = models.DateTimeField(null=True)
    t_time = models.DateTimeField(null=True)
    status = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name='未开始') 
    class Meta:
        db_table = 'task_point'
        ordering = ['status']
