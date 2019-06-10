from django.db import models

class UserInfo(models.Model):
    '''用户表'''
    username = models.CharField(max_length=128,unique=True)
    nickname = models.CharField(max_length=128,verbose_name="昵称", default="")
    cellphone = models.CharField(max_length=11, verbose_name="手机号码", default="")
    remark = models.CharField(max_length=244, verbose_name="简介备注",  default="")
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    active = models.BooleanField(default='0')
    c_time = models.DateTimeField(null=False)
    l_time = models.DateTimeField(null=True)
    Avatar = models.ImageField(upload_to='Avatar',unique=False,default="/Avatar/cat.jpg")
    Avatar_name = models.CharField(max_length=128,default="cat.jpg")
    class Meta:
        db_table = 'UserInfo'
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
