from collections.abc import Iterable
from django.db import models
import uuid
from catogry.models import Catogry
from django.contrib.auth.models import User
from .Helper import user
from django.db.models import Manager,QuerySet
# Create your models here.

class ModelDevice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50,unique=True)
    catogry = models.ForeignKey(Catogry,related_name="modal",null=True,blank=True,on_delete=models.CASCADE)
    min_device = models.IntegerField("Minimum number of devices for alerting",default=1)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ubdate_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    def __str__(self):
        return self.name
    
class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50,unique=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ubdate_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    def __str__(self):
        return self.name

class DeviceFile(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    file = models.FileField(upload_to="file/%d")
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ubdate_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    
StatusName = {1:'Available',2:'Given',3:'Servicing',4:'expired',5:'broken'}

class DeviceManager(Manager):
    def get_queryset(self):
        return QuerySet(self.model, using=self._db).exclude(deleted=True)
    
class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catogry = models.ForeignKey(Catogry ,null=True,on_delete=models.CASCADE)
    service_tag = models.CharField(max_length=150,unique=True)
    modal = models.ForeignKey(ModelDevice ,related_name='device',null=True,on_delete=models.SET_NULL)
    store =  models.ForeignKey(Store,related_name='device',null=True, on_delete=models.SET_NULL)
    purchase_date = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    supplier = models.CharField(max_length=50,null=True,blank=True)
    status = models.IntegerField(default=1)
    file = models.ForeignKey(DeviceFile,null=True,blank=True, on_delete=models.SET_NULL)
    Warranty_date = models.DateField(null=True,blank=True)
    type_device = models.CharField(choices= [('office','office'),('Personal','Personal')],default='Personal', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ubdate_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    created_by = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    deleted = models.BooleanField(default = False)
    objects = DeviceManager()
    def status_name(self):
        return StatusName[self.status]
    
    
class Employee(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50)
    zalaf_id = models.CharField(unique=True,max_length=50)
    email = models.EmailField(unique=True,max_length=254)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ubdate_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    

class EmployeeDevice(models.Model):
    employee = models.UUIDField(editable=False)
    device = models.ForeignKey(Device,related_name='emp_device',on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ubdate_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    def formatted_created_at(self):
        # Format the datetime field using isoformat()
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')
    
    def save(self, *args, **kwargs):
        # Custom logic before saving
       
        super(EmployeeDevice, self).save(*args, **kwargs)
        
class Departments(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def CountConnect(self):
        return len(self.office_set.all()) + len(self.deprt_device.all())

class Office(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    
class DeprtDevice(models.Model):
    device = models.ForeignKey(Device,related_name='device_depart', on_delete=models.CASCADE)
    departments = models.ForeignKey(Departments,related_name="deprt_device",on_delete=models.CASCADE)
    office = models.ManyToManyField(Office,related_name="deprt_device")
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ubdate_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    def save(self,*args, **kwargs):
        
        return super().save(*args,**kwargs)
    
class HistoryDevice(models.Model):
    device = models.ForeignKey(Device,related_name='history', on_delete=models.CASCADE)
    status = models.CharField(choices=[('1','Working'),('3','Expired'),('4','borken')], max_length=50)
    type = models.CharField(choices=[('1','Employee'),('2','Servicing'),('3','Change status'),('4','Departments')],max_length=50)
    is_from = models.BooleanField(default=False)
    is_to = models.BooleanField(default=False)
    store = models.CharField(null=True ,blank=True ,max_length=50)
    employee = models.UUIDField(editable=False,null=True,blank=True)
    departDevice = models.ForeignKey(DeprtDevice,related_name="depart_device",null=True,blank=True,on_delete=models.CASCADE)
    detiles = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ubdate_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    created_by = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    
    def employeeData(self):
        if self.employee:
            return user(str(self.employee))
    class Meta:
        ordering = ['-created_at']

class ModelSparePart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50,unique=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ubdate_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    def __str__(self):
        return self.name
         
class SparePart(models.Model):    
    service_tag = models.CharField(max_length=150,unique=True,blank=True,null=True)
    descripe = models.TextField(blank=True,null=True)
    model = models.ForeignKey(ModelSparePart,related_name='spare_part', on_delete=models.CASCADE)
    device = models.OneToOneField(Device,null=True,blank=True,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    store = models.ForeignKey(Store,related_name="spare_part", on_delete=models.CASCADE)
    supplier = models.CharField(max_length=50,null=True,blank=True)
    file = models.ForeignKey(DeviceFile,null=True,blank=True, on_delete=models.SET_NULL)
    Warranty_date = models.DateField(null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(null=True,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User, related_name='modyfi_spare',null=True,blank=True,on_delete=models.CASCADE)
    modify_at = models.DateTimeField(auto_now=True)
    
    