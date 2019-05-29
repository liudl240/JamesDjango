from django.db import models

# Create your models here.

class tasks(models.Model):
    '''任务表'''
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128,unique=True)
    content = models.CharField(max_length=128,unique=True)
    tags = models.CharField(max_length=128,unique=True) 
    c_time = models.DateTimeField(null=False)
    f_time = models.DateTimeField(null=True)
    m_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=128,unique=False) 
    
    username = models.ForeignKey('Users.UserInfo',to_field='username',default="1",on_delete=models.CASCADE)
    doc = models.ForeignKey('wiki.doc',to_field='id',default=1,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'tasks'
        ordering = ['c_time']
