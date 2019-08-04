from django.db import models

# Create your models here.

class company(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=200,null=True)
    product = models.CharField(max_length=200,null=True)
    """购买时间""" 
    buy_time = models.CharField(max_length=100,null=True)
    """过期时间""" 
    exprie_time = models.CharField(max_length=100,null=True)
    price = models.CharField(max_length=200,null=False) 
    application  = models.CharField(max_length=200,null=False) 
    num = models.IntegerField(null=False)
    urladdress = models.CharField(max_length=200,null=True)


    class Meta:
        db_table = 'company'
        ordering = ['exprie_time']
