from django.db import models

class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=20)
    username = models.ForeignKey('Users.UserInfo', to_field='username', null=True, on_delete=models.CASCADE)
    doc = models.ForeignKey('wiki.doc', to_field='id',  null=True, on_delete=models.CASCADE)
    class Meta:
        db_table = 'IMG'