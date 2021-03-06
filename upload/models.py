from django.db import models
#img = models.ImageField(upload_to='img')
#    username = models.ForeignKey('Users.UserInfo', to_field='username', null=True, on_delete=models.CASCADE)
#    doc = models.ForeignKey('wiki.doc', to_field='id',  null=True, on_delete=models.CASCADE)

class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=128)
    task = models.ForeignKey('Task.tasks',to_field='id',null=True,on_delete=models.CASCADE)
    active = models.CharField(max_length=128,null=True)
    class Meta:
        db_table = 'IMG'
