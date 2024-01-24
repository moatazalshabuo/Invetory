from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserInfo(models.Model):
    id_user = models.CharField(max_length=250)
    user = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE)
    
    
class EmailSenderTo(models.Model):
    email = models.EmailField()
    