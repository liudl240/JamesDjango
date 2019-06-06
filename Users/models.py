from django.db import models

class UserInfo(models.Model):
    '''用户表'''
    username = models.CharField(max_length=128,unique=True)
    nickname = models.CharField(max_length=128,null=True)
    remark = models.CharField(max_length=244,null=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    active = models.BooleanField(default='0')
    c_time = models.DateTimeField(null=False)
    l_time = models.DateTimeField(null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'UserInfo'
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
