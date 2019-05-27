from django.db import models

# Create your models here.
class servicelist(models.Model):
    '''生产跳转链接'''
    title = models.CharField(max_length=128,unique=True)
    desLink = models.CharField(max_length=256)
    jumpLink = models.CharField(max_length=254,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'servicelist'
