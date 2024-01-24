from django.db import models
import uuid

# Create your models here.

class Catogry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50,unique=True)
    descripe = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ubdate_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    def __str__(self):
        return self.name
    
    def countDevices(self):
        return len(self.device_set.all())