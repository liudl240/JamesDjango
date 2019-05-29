from django.db import models

class doc(models.Model):
    '''文章'''
    title = models.EmailField(unique=True)
    active = models.BooleanField(default='0')
    c_time = models.DateTimeField(null=False)
    l_time = models.DateTimeField(null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'doc'
        ordering = ['c_time']

