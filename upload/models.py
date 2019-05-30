from django.db import models

class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=20)
    username = models.ForeignKey('Users.UserInfo', to_field='username', default="1", on_delete=models.CASCADE)
    doc = models.ForeignKey('wiki.doc', to_field='id', default=1, on_delete=models.CASCADE)
    class Meta:
        db_table = 'IMG'