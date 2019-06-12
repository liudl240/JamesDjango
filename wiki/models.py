from django.db import models

class doc(models.Model):
    '''文章'''
    #title = models.EmailField(unique=True)
    
    title = models.TextField(max_length=128)
    c_time = models.DateTimeField(null=False)
    m_time = models.DateTimeField(null=True)
    content =models.TextField(default="",verbose_name='内容')
    username = models.ForeignKey('Users.UserInfo',to_field='username',null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'doc'
        ordering = ['c_time']
